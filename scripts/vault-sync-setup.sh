#!/bin/bash
# ============================================================
# Obsidian Vault 双向同步设置脚本
# VPS ↔ GitHub (private) ↔ 本地 Mac
# ============================================================
#
# 使用方式：
#   1. 先在 VPS 上运行:  bash vault-sync-setup.sh vps
#   2. 再在本地 Mac 运行: bash vault-sync-setup.sh local
#
# 前提条件：
#   - GitHub 已创建私有 repo: szdbetter/obsidian-vault
#   - VPS 和 本地 Mac 都已配置 GitHub SSH key
# ============================================================

set -e

# ── 配置 ──────────────────────────────────────────────────
GITHUB_REPO="git@github.com:szdbetter/obsidian-vault.git"
VPS_VAULT_DIR="/root/.openclaw/obsidian-vault"
LOCAL_VAULT_DIR="/Users/kimi/Desktop/Jimmy/个人文档/Obsidian"
SYNC_INTERVAL_MINUTES=10
# ─────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ============================================================
# VPS 设置
# ============================================================
setup_vps() {
    log "开始 VPS 端设置..."

    # 检查 vault 目录
    if [ ! -d "$VPS_VAULT_DIR" ]; then
        err "Vault 目录不存在: $VPS_VAULT_DIR"
    fi

    cd "$VPS_VAULT_DIR"

    # 初始化 git（如果还没有）
    if [ ! -d ".git" ]; then
        log "初始化 Git 仓库..."
        git init

        # 创建 .gitignore
        cat > .gitignore << 'GITIGNORE'
# Obsidian 配置（每台设备不同，不同步）
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
.DS_Store

# 生成的站点文件（由 generate.py 处理，在另一个 repo）
# 不在这里管理
GITIGNORE

        git add -A
        git commit -m "init: obsidian vault 初始化"
        log "Git 仓库初始化完成"
    else
        warn "Git 仓库已存在，跳过初始化"
    fi

    # 设置远程仓库
    if git remote get-url origin &>/dev/null; then
        warn "远程仓库已设置: $(git remote get-url origin)"
        read -p "是否更新为 $GITHUB_REPO? (y/N) " yn
        if [ "$yn" = "y" ] || [ "$yn" = "Y" ]; then
            git remote set-url origin "$GITHUB_REPO"
            log "远程仓库已更新"
        fi
    else
        git remote add origin "$GITHUB_REPO"
        log "远程仓库已添加: $GITHUB_REPO"
    fi

    # 推送
    log "推送到 GitHub..."
    git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || {
        # 如果远程已有内容，先 pull
        warn "远程已有内容，尝试合并..."
        git pull origin main --allow-unrelated-histories 2>/dev/null || \
        git pull origin master --allow-unrelated-histories 2>/dev/null
        git push -u origin main 2>/dev/null || git push -u origin master
    }
    log "推送完成"

    # 创建自动同步脚本
    SYNC_SCRIPT="/root/.openclaw/vault-auto-sync.sh"
    cat > "$SYNC_SCRIPT" << 'SYNC'
#!/bin/bash
# Obsidian Vault 自动同步脚本
cd /root/.openclaw/obsidian-vault || exit 1

# 先拉取远程更新
git pull --rebase origin main 2>/dev/null || git pull --rebase origin master 2>/dev/null

# 检查是否有本地变更
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M') from VPS"
    git push origin main 2>/dev/null || git push origin master 2>/dev/null
fi
SYNC
    chmod +x "$SYNC_SCRIPT"
    log "自动同步脚本已创建: $SYNC_SCRIPT"

    # 设置 cron job
    CRON_JOB="*/${SYNC_INTERVAL_MINUTES} * * * * $SYNC_SCRIPT >> /root/.openclaw/vault-sync.log 2>&1"

    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "vault-auto-sync"; then
        warn "Cron job 已存在，更新中..."
        crontab -l 2>/dev/null | grep -v "vault-auto-sync" | { cat; echo "$CRON_JOB"; } | crontab -
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    fi
    log "Cron job 已设置: 每 ${SYNC_INTERVAL_MINUTES} 分钟自动同步"

    echo ""
    log "========================================="
    log "VPS 端设置完成！"
    log "========================================="
    echo ""
    echo "  Vault 目录: $VPS_VAULT_DIR"
    echo "  自动同步:   每 ${SYNC_INTERVAL_MINUTES} 分钟"
    echo "  同步日志:   /root/.openclaw/vault-sync.log"
    echo ""
    echo "  下一步: 在本地 Mac 运行:"
    echo "    bash vault-sync-setup.sh local"
    echo ""
}

# ============================================================
# 本地 Mac 设置
# ============================================================
setup_local() {
    log "开始本地 Mac 设置..."

    # 创建目录（如果不存在）
    if [ ! -d "$LOCAL_VAULT_DIR" ]; then
        log "创建 Obsidian 目录: $LOCAL_VAULT_DIR"
        mkdir -p "$LOCAL_VAULT_DIR"
    fi

    # 检查是否已有内容
    if [ -d "$LOCAL_VAULT_DIR/.git" ]; then
        warn "目录已是 Git 仓库，执行 pull..."
        cd "$LOCAL_VAULT_DIR"
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
        log "已同步最新内容"
    elif [ "$(ls -A "$LOCAL_VAULT_DIR" 2>/dev/null)" ]; then
        # 目录非空但不是 git repo
        warn "目录非空，将备份现有内容后克隆..."
        BACKUP_DIR="${LOCAL_VAULT_DIR}_backup_$(date +%Y%m%d%H%M)"
        mv "$LOCAL_VAULT_DIR" "$BACKUP_DIR"
        log "已备份到: $BACKUP_DIR"

        git clone "$GITHUB_REPO" "$LOCAL_VAULT_DIR"
        log "克隆完成"

        # 把备份中的非冲突文件复制回来
        warn "请手动检查备份目录，将需要的文件合并回来:"
        echo "  备份: $BACKUP_DIR"
        echo "  Vault: $LOCAL_VAULT_DIR"
    else
        log "克隆 vault 到本地..."
        git clone "$GITHUB_REPO" "$LOCAL_VAULT_DIR"
        log "克隆完成"
    fi

    # 创建本地自动同步脚本
    SYNC_SCRIPT="$LOCAL_VAULT_DIR/.obsidian/vault-sync.sh"
    mkdir -p "$LOCAL_VAULT_DIR/.obsidian"
    cat > "$SYNC_SCRIPT" << 'SYNC'
#!/bin/bash
# Obsidian Vault 本地自动同步
VAULT_DIR="/Users/kimi/Desktop/Jimmy/个人文档/Obsidian"
cd "$VAULT_DIR" || exit 1

# 先拉取远程更新
git pull --rebase origin main 2>/dev/null || git pull --rebase origin master 2>/dev/null

# 检查是否有本地变更
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M') from Mac"
    git push origin main 2>/dev/null || git push origin master 2>/dev/null
fi
SYNC
    chmod +x "$SYNC_SCRIPT"

    # macOS launchd 自动同步（比 cron 更适合 Mac）
    PLIST_DIR="$HOME/Library/LaunchAgents"
    PLIST_FILE="$PLIST_DIR/com.clawlabs.vault-sync.plist"
    mkdir -p "$PLIST_DIR"

    cat > "$PLIST_FILE" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clawlabs.vault-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${LOCAL_VAULT_DIR}/.obsidian/vault-sync.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>$((SYNC_INTERVAL_MINUTES * 60))</integer>
    <key>StandardOutPath</key>
    <string>${LOCAL_VAULT_DIR}/.obsidian/sync.log</string>
    <key>StandardErrorPath</key>
    <string>${LOCAL_VAULT_DIR}/.obsidian/sync-error.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
PLIST

    # 加载 launchd job
    launchctl unload "$PLIST_FILE" 2>/dev/null
    launchctl load "$PLIST_FILE"
    log "macOS 后台同步已启动（每 ${SYNC_INTERVAL_MINUTES} 分钟）"

    echo ""
    log "========================================="
    log "本地 Mac 设置完成！"
    log "========================================="
    echo ""
    echo "  Vault 目录:  $LOCAL_VAULT_DIR"
    echo "  自动同步:    每 ${SYNC_INTERVAL_MINUTES} 分钟"
    echo "  同步日志:    $LOCAL_VAULT_DIR/.obsidian/sync.log"
    echo ""
    echo "  现在可以用 Obsidian 打开这个目录了:"
    echo "  Obsidian → Open folder as vault → $LOCAL_VAULT_DIR"
    echo ""
    echo "  或者安装 Obsidian Git 插件（社区插件），"
    echo "  设置自动 pull/push 间隔为 ${SYNC_INTERVAL_MINUTES} 分钟，"
    echo "  效果一样但集成度更高。"
    echo ""
}

# ============================================================
# 主入口
# ============================================================
case "$1" in
    vps)
        setup_vps
        ;;
    local)
        setup_local
        ;;
    *)
        echo "用法: bash vault-sync-setup.sh [vps|local]"
        echo ""
        echo "  vps   - 在 VPS 上运行，初始化并推送到 GitHub"
        echo "  local - 在本地 Mac 上运行，克隆并设置自动同步"
        echo ""
        echo "步骤:"
        echo "  1. 先在 GitHub 创建私有 repo: szdbetter/obsidian-vault"
        echo "  2. 在 VPS 运行:  bash vault-sync-setup.sh vps"
        echo "  3. 在 Mac 运行:  bash vault-sync-setup.sh local"
        ;;
esac
