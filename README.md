# rust-bat

## Running Rust Bats

```
cargo run warmup-1 sleepIn true false
cargo run -- warmup-1 diff21 -71
cargo run string-2 doubleChar The
cargo run string-2 xyBalance somethingxy
cargo run monkeyTrouble monkey_trouble false false
cargo run sumDouble sumDouble 6 6
cargo run icyHot icyHot 101 -1
cargo run loneTeen loneTeen 13 20
cargo run delDel delDel hdelhello
cargo run sumHeighs2 sumHeights2 [5, 3, 6, 7, 2], 0, 4

```

## Testing Rust Bats

```
cargo test
```

## Generating Rust Bat Tests

Use the `printbat_builder.py` script to download the Coding Bat problems for a section and automatically generate unit tests 
based off of the tests Coding Bat exposes.

Example:

```
# Generate tests for an entire section
python src/printbat_builder.py Array-3
# Generate tests for just one problem
python src/printbat_builder.py problem p109660
```
