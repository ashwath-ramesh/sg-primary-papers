#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const DOCS_DIR = path.resolve(ROOT, 'docs');

const ATTR_RE = /\b(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/gi;
const HAS_SCHEME_RE = /^[a-zA-Z][a-zA-Z\d+.-]*:/;

function walkHtmlFiles(dir, out = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkHtmlFiles(full, out);
      continue;
    }
    if (entry.isFile() && entry.name.toLowerCase().endsWith('.html')) {
      out.push(full);
    }
  }
  return out;
}

function isIgnoredLink(link) {
  if (!link) return true;
  const trimmed = link.trim();
  if (!trimmed) return true;
  if (trimmed.startsWith('#')) return true;
  if (trimmed.startsWith('//')) return true;
  if (HAS_SCHEME_RE.test(trimmed)) return true;
  return false;
}

function stripQueryAndHash(link) {
  const hashIdx = link.indexOf('#');
  const queryIdx = link.indexOf('?');

  let end = link.length;
  if (hashIdx >= 0) end = Math.min(end, hashIdx);
  if (queryIdx >= 0) end = Math.min(end, queryIdx);

  return link.slice(0, end);
}

function tryDecode(uriPath) {
  try {
    return decodeURI(uriPath);
  } catch {
    return uriPath;
  }
}

function isInsideDocs(absPath) {
  if (absPath === DOCS_DIR) return true;
  return absPath.startsWith(`${DOCS_DIR}${path.sep}`);
}

function buildCandidates(sourceFile, cleanedLink) {
  const decoded = tryDecode(cleanedLink);
  const isRootRelative = decoded.startsWith('/');
  const trailingSlash = decoded.endsWith('/');

  const targetPart = isRootRelative ? decoded.slice(1) : decoded;
  const baseDir = isRootRelative ? DOCS_DIR : path.dirname(sourceFile);
  const resolved = path.resolve(baseDir, targetPart || '.');

  const candidates = [];
  if (trailingSlash) {
    candidates.push(path.join(resolved, 'index.html'));
    return { candidates, resolved };
  }

  candidates.push(resolved);

  if (!path.extname(resolved)) {
    candidates.push(path.join(resolved, 'index.html'));
    candidates.push(`${resolved}.html`);
  }

  return { candidates, resolved };
}

function existingFile(absPath) {
  try {
    return fs.statSync(absPath).isFile();
  } catch {
    return false;
  }
}

function main() {
  if (!fs.existsSync(DOCS_DIR) || !fs.statSync(DOCS_DIR).isDirectory()) {
    console.error(`Missing docs directory: ${DOCS_DIR}`);
    process.exit(2);
  }

  const htmlFiles = walkHtmlFiles(DOCS_DIR).sort();
  const broken = [];
  let checkedCount = 0;

  for (const sourceFile of htmlFiles) {
    const body = fs.readFileSync(sourceFile, 'utf8');
    // Keep tag attributes but strip inline JS body so template literals like
    // href="${url}" in scripts are not treated as real document links.
    const scanBody = body.replace(/(<script\b[^>]*>)[\s\S]*?(<\/script>)/gi, '$1$2');

    ATTR_RE.lastIndex = 0;
    let match;
    while ((match = ATTR_RE.exec(scanBody)) !== null) {
      const raw = (match[1] ?? match[2] ?? match[3] ?? '').trim();
      if (isIgnoredLink(raw)) continue;

      const cleaned = stripQueryAndHash(raw);
      if (!cleaned) continue;

      const { candidates, resolved } = buildCandidates(sourceFile, cleaned);
      checkedCount += 1;

      let ok = false;
      for (const candidate of candidates) {
        if (!isInsideDocs(candidate)) {
          continue;
        }
        if (existingFile(candidate)) {
          ok = true;
          break;
        }
      }

      if (!ok) {
        broken.push({
          source: path.relative(ROOT, sourceFile),
          link: raw,
          resolved: path.relative(ROOT, resolved),
        });
      }
    }
  }

  if (broken.length > 0) {
    console.error(`Checked ${checkedCount} internal links across ${htmlFiles.length} HTML files.`);
    console.error(`Found ${broken.length} broken internal link(s):`);
    for (const item of broken) {
      console.error(`- ${item.source}: \`${item.link}\` -> ${item.resolved}`);
    }
    process.exit(1);
  }

  console.log(`Docs link check passed: ${checkedCount} internal links across ${htmlFiles.length} HTML files.`);
}

main();
