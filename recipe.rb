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
  'tzdata',
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

execute "Copy go tools to /usr/local/bin" do
    command "cp -fr $(go env GOPATH)/bin/* /usr/local/bin/"
end

execute "Install 1Password CLI" do
  command <<-"EOS"
    export OP_VERSION="v0.10.0"
    curl -sS -o 1password.zip https://cache.agilebits.com/dist/1P/op/pkg/${OP_VERSION}/op_linux_amd64_${OP_VERSION}.zip && \
    unzip 1password.zip op -d /usr/local/bin && \
    rm -f 1password.zip
  EOS
  not_if "test -e /usr/local/bin/op"
end

file "/root/.bootstrap/pull-secrets.sh" do
  mode "0700"
  content <<-"EOS"
#!/bin/bash -eu
echo "Authenticating with 1Password"
export OP_SESSION_my=$(op signin https://my.1password.com upamune@gmail.com --output=raw)
export OP_VAULT="remote-workstation"
echo "Pulling secrets"
op get document 'id_ed25519' --vault "${OP_VAULT}" > id_ed25519
op get document 'gpg.private' --vault "${OP_VAULT}" > gpg.private
op get document 'gpg.public' --vault "${OP_VAULT}" > gpg.public
rm -f ~/.ssh/id_ed25519
ln -sfn $(pwd)/id_ed25519 ~/.ssh/id_ed25519
chmod 0600 ~/.ssh/id_ed25519
gpg --import gpg.private
gpg --import gpg.public
echo "Done!"
EOS
end

directory "/root/.ssh" do
  mode "0700"
end

file "/root/.ssh/config" do
  mode "0600"
  content <<-"EOS"
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
EOS
end

execute "Install SpaceVim" do
  command "curl -sLf https://spacevim.org/install.sh | bash"
  not_if "test -e /root/.SpaceVim"
end

execute "Set correct timezone" do
    command "ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime"
end

