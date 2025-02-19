# Pyenv


## Install

```bash
> brew install pyenv
```

## Environment setting

**/.zshrc setup**

```bash
# vim ~/.zshrc

# ...

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
alias brew='env PATH="${PATH//$(pyenv root)\/shims:/}" brew'
```
