---
title: "Saga Steps"
draft: false
---

A saga step represents one action in a [Saga](saga.md)—a distributed
transaction that coordinates changes across multiple components. Each step
defines both a forward action (`do`) and a compensating action (`undo`) to
enable rollback if later steps fail.

## Purpose

Saga steps provide:

- **Atomic operations**: Each step succeeds or fails as a unit
- **Compensation logic**: Define how to reverse an action if needed
- **Clear sequencing**: Steps execute in defined order
- **Distributed coordination**: Manage state across multiple entities

## Syntax

```riddl
saga ProcessPayment is {
  step ReserveInventory is {
    input: { orderId: OrderId, items: OrderItem* }
    output: { reservationId: ReservationId }

    do {
      tell entity Inventory to ReserveItems
    }

    undo {
      tell entity Inventory to ReleaseReservation
    }
  }

  step ChargePayment is {
    input: { customerId: CustomerId, amount: Money }
    output: { transactionId: TransactionId }

    do {
      tell entity PaymentService to ProcessCharge
    }

    undo {
      tell entity PaymentService to RefundCharge
    }
  }

  step CreateOrder is {
    input: { customerId: CustomerId, items: OrderItem* }
    output: { orderId: OrderId }

    do {
      tell entity OrderService to CreateOrder
    }

    undo {
      tell entity OrderService to CancelOrder
    }
  }
}
```

## Step Components

| Component | Required | Description |
|-----------|----------|-------------|
| `input` | Yes | Data the step receives |
| `output` | Yes | Data the step produces |
| `do` | Yes | Forward action to perform |
| `undo` | Yes | Compensation action for rollback |

## Execution Flow

When a saga executes:

1. Steps run in sequence, each `do` action executing in order
2. If a step fails, the saga reverses direction
3. Each completed step's `undo` action runs in reverse order
4. The saga completes when all compensations finish

```
Normal flow:     Step1.do → Step2.do → Step3.do → Success
Failure at S3:   Step1.do → Step2.do → Step3.do (fails)
                          ↓
Compensation:    Step2.undo → Step1.undo → Saga failed (clean state)
```

## Example: Order Fulfillment Saga

```riddl
saga FulfillOrder is {
  |Coordinates order fulfillment across inventory,
  |payment, and shipping services.

  step ValidateOrder is {
    input: { orderId: OrderId }
    output: { validated: Boolean }
    do { tell entity OrderValidator to ValidateOrder }
    undo { prompt "No compensation needed for validation" }
  }

  step ReserveStock is {
    input: { orderId: OrderId, items: OrderItem* }
    output: { reservationId: ReservationId }
    do { tell entity Inventory to ReserveItems }
    undo { tell entity Inventory to ReleaseItems }
  }

  step ProcessPayment is {
    input: { orderId: OrderId, amount: Money }
    output: { paymentId: PaymentId }
    do { tell entity PaymentGateway to Charge }
    undo { tell entity PaymentGateway to Refund }
  }

  step ShipOrder is {
    input: { orderId: OrderId, address: Address }
    output: { trackingNumber: String }
    do { tell entity ShippingService to CreateShipment }
    undo { tell entity ShippingService to CancelShipment }
  }
}
```

## Best Practices

1. **Make steps idempotent**: Steps should be safe to retry
2. **Keep steps small**: Each step should do one thing
3. **Design compensations carefully**: Ensure undo truly reverses the action
4. **Handle partial failures**: Some actions can't be fully undone (e.g., sent
   emails)—design accordingly
5. **Log everything**: Saga debugging requires visibility into each step

## Occurs In

* [Sagas](saga.md)

## Contains

* [Statements](statement.md) within `do` and `undo` blocks