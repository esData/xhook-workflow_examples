---
name: ripple-pay_test01.spec
summary: Playground
description: Do anything
uri: https://github.com/esDataCo/tree/master/co-test
publish: private
parameters:
  environment: hooks-testnet-v3.xrpl-labs.com
  secret: snyJzeqYshamkRKrgAqkEu5r84w3b
  destination: rLpj4RNw1M8ZvRt1vnuSLXUWugCGeetAMn
steps:
  account_info_01:
    step: ripple-account_info
  account_info_02:
    step: ripple-account_info
    dependsOn: account_info_01
    parameters:
      account: $[parameters.destination]
  pay01:
    step: ripple-pay
    dependsOn: account_info_02
    delay: 5
    parameters:
      account_sequence: $[steps.account_info_01.outputs.Sequence]
      destination: $[parameters.destination]
      amount: 100
  account_info_01_post:
    dependsOn: pay01
    step: ripple-account_info
    delay: 5
  account_info_02_post:
    dependsOn: account_info_01_post
    step: ripple-account_info
    delay: 5
    parameters:
      account: $[parameters.destination]
  cal_source_balance:
    dependsOn: account_info_02_post
    step: ripple-accept
    parameters:
      amount: >-
        ?[$[steps.account_info_01.outputs.Balance] -
        $[steps.pay01.parameters.amount]]
  inspect_source_account:
    step: ripple-xrpspec
    dependsOn: cal_source_balance
    parameters:
      assertion: toEqual
      object: $[steps.account_info_01_post.outputs.Balance]
      value: >-
        ?[$[steps.cal_source_balance.parameters.amount] -
        $[steps.pay01.outputs.result.tx_json.Fee]]
  inspect_target_account:
    step: ripple-xrpspec
    dependsOn: inspect_source_account
    parameters:
      assertion: toEqual
      object: $[steps.account_info_02_post.outputs.Balance]
      value: >-
        ?[$[steps.account_info_02.outputs.Balance] +
        $[steps.pay01.parameters.amount]]
invokes:
  - workflow

