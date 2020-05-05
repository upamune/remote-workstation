# Packages

execute "Update the package index" do
  command "apt-get update -y"
end

packages = [
  'apt-transport-https',
  'build-essential',
  'ca-certificates',
  'clang',
  'direnv',
  'docker.io',
  'git',
  'gnupg',
  'gnupg2',
  'golang-go',
  'htop',
  'jq',
  'locales',
  'man',
  'mosh',
  'neovim',
  'openssh-server',
  'python',
  'python3',
  'python3-flake8',
  'python3-pip',
  'python3-setuptools',
  'python3-venv',
  'python3-wheel',
  'ripgrep',
  'shellcheck',
  'software-properties-common',
  'sudo',
  'tig',
  'tmux',
  'tree',
  'unzip',
  'vim',
  'vim-gtk3',
  'wget',
  'zip',
  'zsh',
]

packages.each do |p|
  package p
end

execute "Remove apt cacahe" do
  command "rm -rf /var/lib/apt/lists/*"
end

go_packages = [
  'github.com/davidrjenni/reftools/cmd/fillstruct',
  'github.com/mdempsky/gocode',
  'github.com/rogpeppe/godef',
  'github.com/zmb3/gogetdoc',
  'golang.org/x/tools/cmd/goimports',
  'golang.org/x/tools/cmd/gorename',
  'golang.org/x/tools/cmd/guru',
  'golang.org/x/tools/gopls',
  'golang.org/x/lint/golint',
  'github.com/josharian/impl',
  'honnef.co/go/tools/cmd/keyify',
  'github.com/fatih/gomodifytags',
  'github.com/fatih/motion',
  'github.com/koron/iferr',
]

go_packages.each do |p|
  execute "Install #{p}" do
    command "go get #{p}"
  end
end

execute "Install SpaceVim" do
  command "curl -sLf https://spacevim.org/install.sh | bash"
  not_if "test -e /root/.SpaceVim"
end

execute "Copy go tools to /usr/local/bin" do
    command "cp -fr $(go env GOPATH)/bin/* /usr/local/bin/"
end