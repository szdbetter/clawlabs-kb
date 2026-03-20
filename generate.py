#!/usr/bin/env python3
import os
import re
import markdown
import json
from datetime import datetime

VAULT_DIR = "/root/.openclaw/obsidian-vault"
SITE_DIR = "/root/.openclaw/obsidian-vault-site"

# Category mapping
CATEGORIES = {
    "Knowledge/AI": ("AI", 5),
    "Knowledge/Crypto": ("Crypto", 4),
    "Knowledge/Tech": ("Tech", 4),
    "Knowledge/投资": ("投资", 2),
    "Knowledge/Business": ("Business", 1),
    "Projects": ("Projects", 4),
    "Daily": ("Daily", 4),
}

def slugify(name):
    return name.replace(" ", "-").replace("/", "-")

def get_all_md_files():
    files = []
    for root, dirs, filenames in os.walk(VAULT_DIR):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in filenames:
            if f.endswith('.md'):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, VAULT_DIR)
                files.append((rel, full))
    return files

def get_category_info(rel_path):
    if is_moc_file(rel_path):
        return "MOC", "MOC"
    parts = rel_path.split(os.sep)
    if len(parts) >= 2 and parts[0] == "Knowledge":
        return "Knowledge", parts[1]
    elif len(parts) >= 1:
        return parts[0], parts[0]
    return "Other", "Other"

def is_moc_file(rel_path):
    """Check if a file is a MOC (Map of Content) note."""
    return rel_path.startswith("MOC/") or rel_path.startswith("MOC\\")

# ── Wikilink resolution ────────────────────────────────────────────────────────
# Build a lookup: note_name -> slug (for all notes in vault)
_WIKILINK_MAP = {}   # "OpenClaw使用笔记" -> "Knowledge-AI-OpenClaw使用笔记"

def _build_wikilink_map(files):
    for rel, _ in files:
        note_name = rel.replace('.md', '').split('/')[-1]
        slug = slugify(rel.replace('.md', ''))
        _WIKILINK_MAP[note_name] = slug

def resolve_wikilinks(content):
    """Convert [[NoteName]] to clickable HTML anchors."""
    def replacer(match):
        note_name = match.group(1)
        slug = _WIKILINK_MAP.get(note_name)
        if slug:
            return f'<a href="{slug}.html" class="wikilink">{note_name}</a>'
        return f'<span class="wikilink-missing" title="未找到笔记">{note_name}</span>'
    return re.sub(r'\[\[([^\]]+)\]\]', replacer, content)

# ── MOC golden highlighting in nav ───────────────────────────────────────────
MOC_ICON = "🗺️"
MOC_STYLE = 'color: #ffd700; font-weight: bold;'   # golden

def _moc_nav_item(title, rel):
    href = slugify(rel.replace('.md', '')) + '.html'
    return f'<a href="{href}" class="nav-item nav-moc" style="{MOC_STYLE}">{MOC_ICON} {title}</a>\n'

def build_nav_html():
    """Build left sidebar nav grouped by category. MOC notes get golden treatment."""
    groups = {}
    moc_items = []
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, VAULT_DIR)
            cat_folder, cat_name = get_category_info(rel)
            
            title = f.replace('.md', '')
            if is_moc_file(rel):
                moc_items.append((title, rel))
                continue
            
            if cat_folder == "Knowledge":
                group_key = cat_name
                group_label = cat_name
            else:
                group_key = cat_folder
                group_label = cat_folder
            
            if group_label not in groups:
                groups[group_label] = []
            groups[group_label].append((title, rel))
    
    html = '<nav class="sidebar-nav">\n'
    html += f'<a href="index.html" class="nav-home">📚 知识库首页</a>\n'
    
    # MOC section first
    if moc_items:
        html += '<div class="nav-group"><div class="nav-group-title" style="color:#ffd700;">🗺️ MOC</div>\n'
        for title, rel in sorted(moc_items):
            html += _moc_nav_item(title, rel)
        html += '</div>\n'
    
    for group, items in sorted(groups.items()):
        html += f'<div class="nav-group"><div class="nav-group-title">{group}</div>\n'
        for title, rel in sorted(items):
            href = slugify(rel.replace('.md', '')) + '.html'
            html += f'<a href="{href}" class="nav-item">{title}</a>\n'
        html += '</div>\n'
    html += '</nav>'
    return html

def md_to_html(content):
    # Resolve wikilinks first
    content = resolve_wikilinks(content)
    return markdown.markdown(content, extensions=['tables', 'fenced_code', 'codehilite'])

def build_breadcrumb(rel_path):
    parts = rel_path.replace('.md','').split(os.sep)
    crumbs = [('首页', 'index.html')]
    current = []
    for p in parts:
        current.append(p)
        href = slugify('-'.join(current)) + '.html'
        crumbs.append((p, href))
    
    html = '<div class="breadcrumb">'
    for i, (name, href) in enumerate(crumbs):
        if i > 0:
            html += ' <span class="breadcrumb-sep">›</span> '
        if i == len(crumbs) - 1:
            html += f'<span class="breadcrumb-current">{name}</span>'
        else:
            html += f'<a href="{href}">{name}</a>'
    html += '</div>'
    return html

def generate_index(files):
    # Group files by category for stats
    groups = {}
    for rel, full in files:
        cat_folder, cat_name = get_category_info(rel)
        key = cat_name if cat_folder == "Knowledge" else cat_folder
        if key not in groups:
            groups[key] = []
        mtime = os.path.getmtime(full)
        groups[key].append((rel, full, mtime))
    
    total = len(files)
    latest_mtime = max(os.path.getmtime(f[1]) for f in files)
    latest_date = datetime.fromtimestamp(latest_mtime).strftime('%Y-%m-%d %H:%M')
    
    html = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ClawLabs 知识库</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, "Noto Sans SC", "Microsoft YaHei", sans-serif;
  background: #1a1a2e;
  color: #e0e0e0;
  min-height: 100vh;
  display: flex;
}
.sidebar {
  width: 260px;
  min-height: 100vh;
  background: #16162a;
  border-right: 1px solid #2a2a4a;
  padding: 20px 0;
  position: fixed;
  top: 0; left: 0;
  overflow-y: auto;
}
.main {
  margin-left: 260px;
  padding: 40px 60px;
  width: 100%;
  max-width: 1100px;
}
.nav-home {
  display: block;
  padding: 12px 20px;
  color: #fff;
  text-decoration: none;
  font-size: 15px;
  font-weight: bold;
  border-bottom: 1px solid #2a2a4a;
  margin-bottom: 10px;
}
.nav-group { margin-bottom: 5px; }
.nav-group-title {
  padding: 8px 20px 4px;
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.nav-item {
  display: block;
  padding: 6px 20px;
  color: #c0c0d0;
  text-decoration: none;
  font-size: 13px;
  transition: background 0.15s;
}
.nav-item:hover { background: #2a2a4a; color: #fff; }
.index-header { margin-bottom: 40px; }
.index-header h1 {
  font-size: 28px;
  color: #fff;
  margin-bottom: 8px;
}
.index-header .subtitle { color: #888; font-size: 14px; }
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 40px;
}
.stat-card {
  background: #1e1e3a;
  border: 1px solid #2a2a4a;
  border-radius: 8px;
  padding: 20px;
}
.stat-card .stat-num {
  font-size: 32px;
  color: #7fdbca;
  font-weight: bold;
}
.stat-card .stat-label { color: #888; font-size: 13px; margin-top: 4px; }
.file-list { margin-top: 20px; }
.file-group { margin-bottom: 30px; }
.file-group h2 {
  font-size: 16px;
  color: #7fdbca;
  border-bottom: 1px solid #2a2a4a;
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.file-group ul { list-style: none; }
.file-group li { margin-bottom: 4px; }
.file-group a {
  color: #c0c0d0;
  text-decoration: none;
  font-size: 13px;
  display: block;
  padding: 5px 0;
  transition: color 0.15s;
}
.file-group a:hover { color: #fff; }
.file-group .file-meta { color: #666; font-size: 11px; margin-left: 8px; }
@media (max-width: 768px) {
  .sidebar { display: none; }
  .main { margin-left: 0; padding: 20px; }
  .stats { grid-template-columns: 1fr 1fr; }
}
</style>
</head>
<body>
<div class="sidebar">
  <a href="index.html" class="nav-home">📚 知识库首页</a>
  <div class="nav-group"><div class="nav-group-title">Overview</div>
  <a href="index.html" class="nav-item">📊 总览</a>
  </div>
  __NAV__
</div>
<div class="main">
<div class="index-header">
<h1>📚 ClawLabs 知识库</h1>
<p class="subtitle">Obsidian 笔记库 · 共 {total} 篇 · 最后更新 {latest_date}</p>
</div>
<div class="stats">
<div class="stat-card"><div class="stat-num">{total}</div><div class="stat-label">笔记总数</div></div>
__STAT_CARDS__
</div>
<div class="file-list">
__FILE_LIST__
</div>
</div>
</body>
</html>"""
    
    stat_cards = ""
    file_list = ""
    
    # Build stat cards sorted by category
    sorted_cats = sorted(groups.items(), key=lambda x: x[0])
    for cat, items in sorted_cats:
        stat_cards += f'<div class="stat-card"><div class="stat-num">{len(items)}</div><div class="stat-label">{cat}</div></div>\n'
    
    # Build file list grouped
    for cat, items in sorted_cats:
        file_list += f'<div class="file-group"><h2>{cat}</h2><ul>\n'
        for rel, full, mtime in sorted(items, key=lambda x: x[0]):
            title = rel.replace('.md','').split('/')[-1]
            href = slugify(rel.replace('.md', '')) + '.html'
            date = datetime.fromtimestamp(mtime).strftime('%m-%d')
            file_list += f'<li><a href="{href}">{title}</a> <span class="file-meta">{date}</span></li>\n'
        file_list += '</ul></div>\n'
    
    nav_html = build_nav_html()
    page = html.replace('{total}', str(total))
    page = page.replace('{latest_date}', latest_date)
    page = page.replace('__STAT_CARDS__', stat_cards)
    page = page.replace('__FILE_LIST__', file_list)
    page = page.replace('__NAV__', nav_html)
    return page

def generate_article(rel_path, full_path, is_moc=False):
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = rel_path.replace('.md','').split('/')[-1]
    html_content = md_to_html(content)
    breadcrumb = build_breadcrumb(rel_path)
    nav_html = build_nav_html()
    moc_badge = '<span class="moc-badge">🗺️ MOC</span>' if is_moc else ''
    
    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ClawLabs KB</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, "Noto Sans SC", "Microsoft YaHei", sans-serif;
  background: #1a1a2e;
  color: #e0e0e0;
  min-height: 100vh;
  display: flex;
}}
.sidebar {{
  width: 260px;
  min-height: 100vh;
  background: #16162a;
  border-right: 1px solid #2a2a4a;
  padding: 20px 0;
  position: fixed;
  top: 0; left: 0;
  overflow-y: auto;
}}
.nav-home {{
  display: block;
  padding: 12px 20px;
  color: #fff;
  text-decoration: none;
  font-size: 15px;
  font-weight: bold;
  border-bottom: 1px solid #2a2a4a;
  margin-bottom: 10px;
}}
.nav-group {{ margin-bottom: 5px; }}
.nav-group-title {{
  padding: 8px 20px 4px;
  font-size: 11px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
}}
.nav-item {{
  display: block;
  padding: 6px 20px;
  color: #c0c0d0;
  text-decoration: none;
  font-size: 13px;
  transition: background 0.15s;
}}
.nav-item:hover {{ background: #2a2a4a; color: #fff; }}
.main {{
  margin-left: 260px;
  padding: 40px 60px;
  width: 100%;
  max-width: 900px;
}}
.breadcrumb {{
  font-size: 12px;
  color: #666;
  margin-bottom: 24px;
}}
.breadcrumb a {{ color: #7fdbca; text-decoration: none; }}
.breadcrumb a:hover {{ text-decoration: underline; }}
.breadcrumb-sep {{ color: #444; margin: 0 4px; }}
.breadcrumb-current {{ color: #aaa; }}
.article-header {{ margin-bottom: 30px; }}
.article-header h1 {{
  font-size: 26px;
  color: #fff;
  margin-bottom: 8px;
  line-height: 1.3;
}}
.back-link {{
  display: inline-block;
  margin-top: 8px;
  color: #7fdbca;
  text-decoration: none;
  font-size: 13px;
}}
.back-link:hover {{ text-decoration: underline; }}
.article-content {{
  line-height: 1.8;
  font-size: 15px;
}}
.article-content h1, .article-content h2, .article-content h3 {{
  color: #fff;
  margin: 24px 0 12px;
}}
.article-content h1 {{ font-size: 22px; }}
.article-content h2 {{ font-size: 18px; border-bottom: 1px solid #2a2a4a; padding-bottom: 6px; }}
.article-content h3 {{ font-size: 16px; color: #c0c0d0; }}
.article-content p {{ margin-bottom: 14px; }}
.article-content a {{ color: #7fdbca; }}
.article-content code {{
  background: #252540;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  color: #f0c060;
}}
.article-content pre {{
  background: #16162a;
  border: 1px solid #2a2a4a;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
}}
.article-content pre code {{
  background: none;
  color: #c0c0d0;
  padding: 0;
}}
.article-content ul, .article-content ol {{
  margin: 0 0 14px 24px;
}}
.article-content li {{ margin-bottom: 6px; }}
.article-content blockquote {{
  border-left: 3px solid #7fdbca;
  padding: 8px 16px;
  margin: 16px 0;
  background: #1e1e3a;
  color: #c0c0d0;
}}
.article-content table {{
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}}
.article-content th, .article-content td {{
  border: 1px solid #2a2a4a;
  padding: 8px 12px;
  text-align: left;
}}
.article-content th {{ background: #1e1e3a; color: #fff; }}
.article-content tr:nth-child(even) {{ background: #1a1a30; }}
.article-content img {{ max-width: 100%; border-radius: 8px; margin: 12px 0; }}
.article-content hr {{ border: none; border-top: 1px solid #2a2a4a; margin: 24px 0; }}
.article-content .wikilink {{
  color: #7fdbca;
  text-decoration: none;
  border-bottom: 1px dashed #7fdbca;
  padding-bottom: 1px;
}}
.article-content .wikilink:hover {{ border-bottom: 1px solid #7fdbca; }}
.article-content .wikilink-missing {{
  color: #666;
  text-decoration: none;
  border-bottom: 1px dashed #444;
}}
/* MOC title highlight */
.article-content .moc-badge {{
  display: inline-block;
  background: #ffd700;
  color: #1a1a2e;
  font-size: 11px;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}}
@media (max-width: 768px) {{
  .sidebar {{ display: none; }}
  .main {{ margin-left: 0; padding: 20px; }}
}}
</style>
</head>
<body>
<div class="sidebar">
  {nav_html}
</div>
<div class="main">
  {breadcrumb}
  <div class="article-header">
    {moc_badge}
    <h1>{title}</h1>
    <a href="index.html" class="back-link">← 返回首页</a>
  </div>
  <div class="article-content">
    {html_content}
  </div>
</div>
</body>
</html>"""
    return html

def main():
    files = get_all_md_files()
    _build_wikilink_map(files)
    
    # Generate index
    index_html = generate_index(files)
    with open(os.path.join(SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"Generated index.html ({len(files)} files)")
    
    # Generate article pages
    for rel, full in files:
        is_moc = is_moc_file(rel)
        html = generate_article(rel, full, is_moc=is_moc)
        out_name = slugify(rel.replace('.md', '')) + '.html'
        out_path = os.path.join(SITE_DIR, out_name)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  -> {out_name}")
    
    # Print stats
    groups = {}
    for rel, full in files:
        cat_folder, cat_name = get_category_info(rel)
        key = cat_name if cat_folder == "Knowledge" else cat_folder
        groups[key] = groups.get(key, 0) + 1
        _ = cat_folder  # unused but keep for clarity
    
    print(f"\nTotal: {len(files)} notes")
    for cat, count in sorted(groups.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
