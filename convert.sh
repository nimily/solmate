#!/usr/bin/env bash


SUCCESS_EMOJI="\xe2\x9c\x85\x0a"
FAILURE_EMOJI="\xe2\x9d\x8c"

SOLMATE_ROOT=`dirname "$(realpath $0)"`
IDL_ROOT="$SOLMATE_ROOT/programs"


function system_program() {
  # there is some ambiguity re some of the following accounts:
  ROOT_MODULE="solmate.lib.system_program"
  ADDRESSES=(
    PROGRAM_ID=11111111111111111111111111111111
  )

  DEFAULT_ACCOUNTS=(
    program_id=$ROOT_MODULE.addrs.PROGRAM_ID
    rent=solana.sysvar.SYSVAR_RENT_PUBKEY
    clock=solana.sysvar.SYSVAR_CLOCK_PUBKEY
  )

  cd programs
  PYTHONPATH=$SOLMATE_ROOT:$PYTHONPATH python -m system_program_codegen \
    --idl $IDL_ROOT/system_program.json \
    --module $ROOT_MODULE \
    --root-dir $SOLMATE_ROOT \
    --addrs ${ADDRESSES[@]} \
    --default-accounts ${DEFAULT_ACCOUNTS[@]} \
    --instruction-tag "incremental:U32"
  exit_code=$?
  cd ..
  return $exit_code
}


function convert() {
  echo "Converting $1..."
  tput dim
  $1
  exit_code=$?
  tput sgr0
  if test $exit_code -eq 0; then
    echo -e "Code for $1 was generated successfully! $SUCCESS_EMOJI"
  else
    echo -e "An error occurred while generating code for $1! $FAILURE_EMOJI"
    exit 1
  fi
}


convert system_program
