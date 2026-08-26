---
title: "Scheduling Context"
description: "Staff shift planning and time tracking"
---


<!-- riddl-prelude
type ShiftId is Id(Shift)
type EmployeeId is UUID
record StoredShift is { shiftId: ShiftId }
event ShiftCreated is { shiftId: ShiftId }
event EmployeeAssigned is { shiftId: ShiftId }
event AssignEmployeeRejected is { shiftId: ShiftId, rejectionReason: String(1,500) }
type ShiftEvent is ShiftCreated | EmployeeAssigned | AssignEmployeeRejected
entity Shift is { ??? }
repository ShiftRepository is { ??? }
command PersistEmployeeAssigned is { shiftId: ShiftId }
-->

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

<!-- riddl: in-context no-prelude=ShiftId,EmployeeId -->
```riddl
type ShiftId is Id(Shift)

type EmployeeId is UUID
```

The `ShiftRole` enumeration maps directly to the personas
interviewed — Host, Server, Bartender, Chef, Cook — plus
Dishwasher and Manager.

## Entity: Shift

The `Shift` entity has a 6-command lifecycle:

<!-- riddl: in-context no-prelude=Shift,ShiftCreated,EmployeeAssigned,AssignEmployeeRejected,ShiftCommand,ShiftEvent -->
```riddl
event-sourced entity Shift as flow is {

  // An event-sourced entity OWNS the commands and events that change it, so
  // they are declared INSIDE it, and every command names the event it yields.
  command CreateShift yields event ShiftCreated is { shiftId: ShiftId }
  command AssignEmployee yields event EmployeeAssigned is { shiftId: ShiftId }

  event ShiftCreated is { shiftId: ShiftId }
  event EmployeeAssigned is { shiftId: ShiftId }
  event AssignEmployeeRejected is { shiftId: ShiftId, rejectionReason: String(1,500) }

  record ShiftData is { shiftId: ShiftId }

  // Lifecycle phases are named STATES, not a status field: each state
  // declares the commands it accepts, so the compiler knows the machine.
  initial state ActiveShift of record ShiftData is {
    handler ActiveShiftHandler is {
      on cmd: command AssignEmployee is {
        yield event EmployeeAssigned(shiftId = cmd.shiftId)
      }
      // `set` and `morph` may appear ONLY in an `on event` clause here:
      // replay has to re-apply exactly the same change.
      on evt: event EmployeeAssigned is {
        morph entity Shift to state Filled
          with record ShiftData(shiftId = evt.shiftId)
      }
    }
  }

  state Filled of record ShiftData is {
    handler FilledHandler is {
      // A command this state does not accept is refused -- and the refusal
      // is PUBLISHED before it is raised, so the attempt is recorded.
      on cmd: command AssignEmployee is {
        send event AssignEmployeeRejected(shiftId = cmd.shiftId,
          rejectionReason = "Shift does not accept AssignEmployee in this state")
          to outlet ShiftEvents
        error "Shift does not accept AssignEmployee in this state"
      }
    }
  }

  // A processor receives on its OWN inlet and publishes on its OWN outlet,
  // and a portlet's type must ADMIT everything that travels on it.
  type ShiftCommand is CreateShift | AssignEmployee
  type ShiftEvent is ShiftCreated | EmployeeAssigned | AssignEmployeeRejected

  inlet ShiftCommands is type ShiftCommand
  outlet ShiftEvents is type ShiftEvent
}
```

The lifecycle: **Create → Assign Employee → Clock In → Clock
Out** (with optional **Swap** or **Cancel** at any point).

The `SwapShift` command tracks both the original and replacement
employee, maintaining an audit trail of who was originally
assigned. This matters for labor compliance and reporting.

## Repository

<!-- riddl: in-context no-prelude=ShiftRepository,StoredShift,PersistEmployeeAssigned -->
```riddl
repository ShiftRepository as flow is {
  inlet ShiftRepositoryFromShift is command PersistEmployeeAssigned
  outlet ShiftRepositoryResponses is result ShiftResult

  // A repository answers with a RESULT, never an event.
  result ShiftResult is { found: Boolean }

  record StoredShift is { shiftId: ShiftId }

  // A repository that answers queries and declares NO index at all is a
  // sequential scan by construction, and draws a warning saying so.
  schema ShiftSchema is relational
    of rows as record StoredShift
      index on field StoredShift.shiftId

  command PersistEmployeeAssigned is { shiftId: ShiftId }

  handler ShiftPersistence is {
    on command PersistEmployeeAssigned is {
      do "update the stored shift row for this shiftId"
    }
    // An inlet admitting an alternation needs a clause that receives it.
    // Handling each member is not enough -- say what ARRIVING means.
    on other is {
      do "persist whatever else arrives on this inlet"
    }
  }
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
