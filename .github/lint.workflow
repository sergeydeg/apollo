workflow "Python black lint" {
  resolves = ["Lint"]
  on = "push"
}

action "Lint" {
  uses = "lgeiger/black-action@master"
  args = ". --check"
}
