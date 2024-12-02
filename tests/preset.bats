#!/usr/bin/env bash

setup() {
    bats_load_library bats-assert
    bats_load_library bats-file
    bats_load_library bats-support

    if [ -f /usr/local/bin/getansible.sh ]; then
        chmod +x /usr/local/bin/getansible.sh
    fi

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
@test "T001: preset" {
    run preset
    assert_failure 1
    assert_output --partial "Usage: preset"
    assert_teardown
}

# bats test_tags=T002
@test "T002: preset with insufficient arguments" {
    run preset -- collection
    assert_failure 1
    assert_output --partial "Usage: preset"
    assert_teardown
}

# bats test_tags=T003
@test "T003: preset with nonexistent collection" {
    run preset -- /nonexistent/collection playbook.yml
    assert_failure
    assert_output --partial "Collection not found"
    assert_teardown
}

# bats test_tags=T004
@test "T004: preset with correct collection" {
    run preset -- /opt/presets /opt/presets/playbooks/ping.yml
    assert_success
    assert_teardown
}
