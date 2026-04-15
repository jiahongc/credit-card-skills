#!/usr/bin/env bash
# Credit Card Skills — installer
#
# One-liner usage (run from your project root):
#   bash <(curl -fsSL https://raw.githubusercontent.com/jiahongc/credit-card-skills/main/install.sh)
#
# Flags:
#   --claude    Install for Claude Code only  → .claude/skills/
#   --codex     Install for OpenAI Codex only → .agents/skills/
#   --all       Install for both
#   (default)   Auto-detects based on existing directories

set -euo pipefail

REPO_URL="https://github.com/jiahongc/credit-card-skills.git"

# ── Colors ────────────────────────────────────────────────────────────────────
bold=$'\033[1m'; reset=$'\033[0m'
blue=$'\033[1;34m'; green=$'\033[1;32m'; yellow=$'\033[1;33m'; red=$'\033[1;31m'
info()    { echo "${blue}→${reset} $*"; }
success() { echo "${green}✓${reset} $*"; }
warn()    { echo "${yellow}!${reset} $*"; }
die()     { echo "${red}✗${reset} $*" >&2; exit 1; }

# ── Args ──────────────────────────────────────────────────────────────────────
MODE="auto"
for arg in "$@"; do
  case "$arg" in
    --claude) MODE="claude" ;;
    --codex)  MODE="codex"  ;;
    --all)    MODE="all"    ;;
  esac
done

# ── Prereqs ───────────────────────────────────────────────────────────────────
command -v git >/dev/null 2>&1 || die "git is required but not found."

# ── Clone into temp dir ───────────────────────────────────────────────────────
TMPDIR_SKILLS=$(mktemp -d)
trap 'rm -rf "$TMPDIR_SKILLS"' EXIT

info "Fetching skills from GitHub..."
git clone --depth=1 --quiet "$REPO_URL" "$TMPDIR_SKILLS" 2>/dev/null \
  || die "Failed to clone $REPO_URL — check your internet connection."
success "Fetched."

# ── Install function ──────────────────────────────────────────────────────────
install_into() {
  local dest="$1"
  local label="$2"
  mkdir -p "$dest"
  cp -R "$TMPDIR_SKILLS"/.claude/skills/card-* "$dest/"
  local count
  count=$(ls -d "$dest"/card-* 2>/dev/null | wc -l | tr -d ' ')
  success "Installed ${bold}${count} skills${reset} → ${dest}  (${label})"
}

# ── Detect targets ────────────────────────────────────────────────────────────
installed=0

install_claude() { install_into ".claude/skills" "Claude Code"; installed=1; }
install_codex()  { install_into ".agents/skills"  "OpenAI Codex"; installed=1; }

case "$MODE" in
  claude) install_claude ;;
  codex)  install_codex  ;;
  all)    install_claude; install_codex ;;
  auto)
    [[ -d ".claude" ]] && install_claude
    [[ -d ".agents" ]] && install_codex
    if [[ "$installed" -eq 0 ]]; then
      warn "No agent directory detected in the current directory."
      warn "Run from your project root, or pass a flag explicitly:"
      echo
      echo "  --claude    → installs to .claude/skills/  (Claude Code)"
      echo "  --codex     → installs to .agents/skills/  (OpenAI Codex)"
      echo "  --all       → installs to both"
      exit 1
    fi
    ;;
esac

# ── Done ──────────────────────────────────────────────────────────────────────
commands=(
  "/card-full [card]              full card report"
  "/card-rate [card]              earning rates"
  "/card-transfer [card]          transfer partners"
  "/card-credits [card]           statement credits"
  "/card-news [card]              recent news (last 3 months)"
  "/card-compare [card] vs [card] side-by-side comparison"
  "/card-value [card]             first-year value estimate"
  "/card-wallet [card], [card]... wallet audit"
  "/card-profile-recommend [...] keep/drop/add recommendations"
)

echo
echo "  ${bold}Commands ready:${reset}"
for command in "${commands[@]}"; do
  echo "    $command"
done
echo
