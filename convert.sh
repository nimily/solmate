#!/usr/bin/env bash


SUCCESS_EMOJI="\xe2\x9c\x85\x0a"
FAILURE_EMOJI="\xe2\x9d\x8c"

SOLMATE_ROOT=`dirname "$(realpath $0)"`
IDL_ROOT="$SOLMATE_ROOT/programs"


function system_program() {
  ROOT_MODULE="solmate.programs.system_program"
  ADDRESSES=(
    PROGRAM_ID=11111111111111111111111111111111
  )

  DEFAULT_ACCOUNTS=(
    program_id=$ROOT_MODULE.addrs.PROGRAM_ID
    recent_blockhashes_sysvar=solana.sysvar.SYSVAR_RECENT_BLOCKHASHES_PUBKEY
    rent_sysvar=solana.sysvar.SYSVAR_RENT_PUBKEY
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


function token_program() {
  ROOT_MODULE="solmate.programs.token_program"
  ADDRESSES=(
    PROGRAM_ID=TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
    # list of famous coins
    USDC_MINT=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
    USDT_MINT=Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB
    SOL_MINT=So11111111111111111111111111111111111111112
    MSOL_MINT=mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So
    JSOL_MINT=7Q2afV64in6N6SeZsAAB81TJzwDoD6zpqmHkzi9Dcavn
    ST_SOL_MINT=7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj
    SRM_MINT=SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt
    MNGO_MINT=MangoCzJ36AjZyKwVj3VnYU4GTonjfVEnJmvvWaxLac
    RAY_MINT=4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R
    MNDE_MINT=MNDEFzGvMt87ueuHvVU9VcTqsAP5b3fTGPsHuuPA5ey
    SLND_MINT=SLNDpmoWTVADgEdndyvWzroNL7zSi1dF9PC3xHGtPwp
    REN_BTC_MINT=CDJWUqTcYTVAKXAVXoQZFes5JUFc7owSeq7eMQcDSbo5
    REN_DOGE_MINT=ArUkYE2XDKzqy77PRRGjo4wREWwqk6RXTfM9NeqzPvjU
    LUNA_WORMHOLE_MINT=F6v4wfAdJB8D8p77bMXZgYt8TDKsYxLYxH5AFhUkYx9W
    ETH_WORMHOLE_MINT=7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs
    BTC_WORMHOLE_MINT=9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E
    BNB_WORMHOLE_MINT=9gP2kCy3wA1ctvYWQk75guqXuHfrEomqydHLtcTCqiLa
    ETH_SOLLET_MINT=2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk
    ALEPH_SOLLET_MINT=CsZ5LZkDS7h9TDKjrbL7VAwQZ9nsRu8vJLhRYfmGaN8K
    HXRO_SOLLET_MINT=DJafV9qemGp7mLMEn5wrfqaFwxsbLgUsGVS16zKRk9kc
  )

  DEFAULT_ACCOUNTS=(
    program_id=$ROOT_MODULE.addrs.PROGRAM_ID
    rent_sysvar=solana.sysvar.SYSVAR_RENT_PUBKEY
  )

  cd programs
  PYTHONPATH=$SOLMATE_ROOT:$PYTHONPATH python -m token_program_codegen \
    --idl $IDL_ROOT/token_program.json \
    --module $ROOT_MODULE \
    --root-dir $SOLMATE_ROOT \
    --addrs ${ADDRESSES[@]} \
    --default-accounts ${DEFAULT_ACCOUNTS[@]} \
    --instruction-tag "incremental:U8" \
    --account-tag "incremental:U8"
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
convert token_program

black solmate/programs
