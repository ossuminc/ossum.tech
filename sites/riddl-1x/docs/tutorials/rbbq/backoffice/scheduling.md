---
title: "Scheduling Context"
description: "Staff shift planning and time tracking"
---

# Scheduling Context

The Scheduling context manages staff shift planning, assignment,
time tracking, shift swaps, and coverage. It provides the
foundation for labor reporting in the
[Reporting](reporting.md) context.

## Purpose

Every restaurant location needs to schedule staff across roles
(host, server, bartender, chef, cook, dishwasher, manager).
The Scheduling context handles the lifecycle of each shift from
creation through assignment, clock-in/out, and potential swaps
or cancellations.

## Types

```riddl
type ShiftId is Id(Scheduling.Shift) with {
  briefly "Shift identifier"
  described by "Unique identifier for a shift."
}

type EmployeeId is UUID with {
  briefly "Employee identifier"
  described by "Unique identifier for an employee."
}

type ShiftStatus is any of {
  ScheduledStatus,
  AssignedStatus,
  InProgressStatus,
  ShiftCompletedStatus,
  ShiftCancelledStatus
} with {
  briefly "Shift status"
  described by "Current status of a shift."
}

type ShiftRole is any of {
  HostRole,
  ServerRole,
  BartenderRole,
  ChefRole,
  CookRole,
  DishwasherRole,
  ManagerRole
} with {
  briefly "Shift role"
  described by "The role for this shift."
}
```

The `ShiftRole` enumeration maps directly to the personas
interviewed — Host, Server, Bartender, Chef, Cook — plus
Dishwasher and Manager.

## Entity: Shift

The `Shift` entity has a 6-command lifecycle:

```riddl
entity Shift is {

  command CreateShift is {
    shiftId is ShiftId
    shiftDate is Date
    shiftStart is TimeStamp
    shiftEnd is TimeStamp
    shiftRole is ShiftRole
  }

  command AssignEmployee is {
    shiftId is ShiftId
    employeeId is EmployeeId
    employeeName is String(1, 100)
  }

  command SwapShift is {
    shiftId is ShiftId
    originalEmployeeId is EmployeeId
    replacementEmployeeId is EmployeeId
    replacementName is String(1, 100)
  }

  command ClockIn is {
    shiftId is ShiftId
    clockedInAt is TimeStamp
  }

  command ClockOut is {
    shiftId is ShiftId
    clockedOutAt is TimeStamp
  }

  command CancelShift is {
    shiftId is ShiftId
    shiftCancelReason is String(1, 500)
  }

  // Events: ShiftCreated, EmployeeAssigned, ShiftSwapped,
  //         ClockedIn, ClockedOut, ShiftCancelled

  state ActiveShift of Shift.ShiftStateData

  handler ShiftHandler is {
    on command CreateShift {
      morph entity Scheduling.Shift to state
        Scheduling.Shift.ActiveShift
        with command CreateShift
      tell event ShiftCreated to
        entity Scheduling.Shift
    }
    on command AssignEmployee {
      tell event EmployeeAssigned to
        entity Scheduling.Shift
    }
    on command SwapShift {
      tell event ShiftSwapped to
        entity Scheduling.Shift
    }
    on command ClockIn {
      tell event ClockedIn to
        entity Scheduling.Shift
    }
    on command ClockOut {
      tell event ClockedOut to
        entity Scheduling.Shift
    }
    on command CancelShift {
      tell event ShiftCancelled to
        entity Scheduling.Shift
    }
  }
}
```

The lifecycle: **Create → Assign Employee → Clock In → Clock
Out** (with optional **Swap** or **Cancel** at any point).

The `SwapShift` command tracks both the original and replacement
employee, maintaining an audit trail of who was originally
assigned. This matters for labor compliance and reporting.

## Repository

```riddl
repository ShiftRepository is {
  schema ShiftData is relational
    of shifts as Shift
    index on field Shift.shiftId
    index on field Shift.shiftDate
    index on field Shift.employeeId
}
```

The index on `shiftDate` enables schedule-by-day views. The
index on `employeeId` supports employee-centric schedule views
("What are my shifts this week?").

## Design Decisions

**Why no projectors?** The Scheduling context is focused on
write operations — creating and managing shifts. The
schedule *view* could be a projector, but the
[Reporting](reporting.md) context already handles the read-model
side with the `LaborReport` projector that listens to
scheduling events.

**Foundation for labor reporting:** The `ClockedIn` and
`ClockedOut` events flow to the Reporting context's
`LaborReport` projector, which calculates hours worked,
completed shifts, and average shift duration. Scheduling
doesn't need to know about reports — it just emits events.

## Source

- [`SchedulingContext.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/SchedulingContext.riddl)
- [`scheduling-types.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/scheduling-types.riddl)
- [`Shift.riddl`](https://github.com/ossuminc/riddl-models/tree/main/hospitality/food-service/reactive-bbq/backoffice/Shift.riddl)
