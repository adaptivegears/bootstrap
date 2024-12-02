#!/usr/bin/env bash

setup() {
    bats_load_library bats-assert
    bats_load_library bats-file
    bats_load_library bats-support

    if [ -n "$TMPDIR" ]; then
      export TMPDIR="$TMPDIR/bats"
    else
      export TMPDIR="/tmp/bats"
    fi
    mkdir -p $TMPDIR
}

assert_teardown() {
    run test -z "$(ls -A $TMPDIR | grep -v 'bats-')"
    assert_success
}

# bats test_tags=T001
@test "T001: bootstrap" {
    run bootstrap
    assert_failure 1
    assert_output --partial "Usage: bootstrap"
    assert_teardown
}

# bats test_tags=T002
@test "T002: bootstrap with insufficient arguments" {
    run bootstrap -- collection
    assert_failure 1
    assert_output --partial "Usage: bootstrap"
    assert_teardown
}

# bats test_tags=T003
@test "T003: bootstrap with nonexistent collection" {
    run bootstrap -- /nonexistent/collection playbook.yml
    assert_failure
    assert_output --partial "Collection not found"
    assert_teardown
}

# bats test_tags=T004
@test "T004: bootstrap with correct collection" {
    run bootstrap -- /opt/collection /opt/collection/playbooks/ping.yml
    assert_success
    assert_teardown
}

# bats test_tags=T005
@test "T005: bootstrap with GitHub collection" {
    run bootstrap -- @andreygubarev/ping
    assert_success
    assert_teardown
}
