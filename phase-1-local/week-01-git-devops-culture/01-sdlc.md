# SDLC — Software Development Life Cycle

## What Does SDLC Mean?

SDLC stands for **Software Development Life Cycle**. In simple words, it's just the list of steps a team follows to turn an idea into working software — from the very first idea, all the way to a finished product that people can actually use.

There are six main steps:

**Plan → Design → Code → Test → Deploy → Monitor**

You'll also hear the word **DevOps**. DevOps is just a way of working where the people who build the software and the people who run it work closely together, so the team can release software faster, with fewer mistakes, and keep it running safely.

---

## Why Is SDLC Important?

Building software sounds simple, but a lot can go wrong along the way:

- What the customer wants might change halfway through
- Many different people and teams need to work together
- New technology can appear and change how things are done
- The project can end up costing more than planned
- Security problems can be found
- Developers might misunderstand what the customer actually needed

Following the SDLC steps helps avoid these problems. Each step has a clear job and a clear result, so the team always knows what to do next — and the project stays easier to plan, track, and keep safe.

---

## The Six Steps, Explained Simply

### 1. Planning

This is where the team figures out what they're building and why, before writing a single line of code.

The team asks simple questions like:

- What problem are we solving?
- Who is going to use this?
- What features does it need to have?
- How much will it cost, and how long will it take?
- How many people do we need to build it?
- What could go wrong along the way?
- What tools or technology should we use?

If the team has a DevOps engineer, they also think ahead about things like: where will this software actually run (for example, on a cloud service), and how will the team know if something breaks later?

> **In one line:** Planning answers *"What should we build?"*

### 2. Design

Now the team decides how the software will actually look and work, before anyone starts coding.

This includes things like:

- What the screens will look like for the people using it
- How the different parts of the system will be organized
- Where information will be stored
- How the pieces will talk to each other safely

For example, a team might decide to build the website with React, handle the background logic with Python, and store data in a database called PostgreSQL. These are just common tool choices — the important part is that the team agrees on a plan before building, so nothing important gets missed.

A simple version of how the pieces connect might look like this:

```
Users
  ↓
Load Balancer   (directs visitors to the right place)
  ↓
The Application (the actual program running)
  ↓
Database        (where information is stored)
```

> **In one line:** Design answers *"How will we build it?"*

### 3. Coding

This is the step most people picture when they think of "programming" — developers actually write the software, following the plan and design from the steps before.

Most teams use a tool called **Git** to manage the code. Think of Git like a save system in a video game: it keeps a record of every change, so if something breaks, the team can always go back to a version that worked. It also lets several developers work on the same project at the same time, without overwriting each other's work.

A typical workflow looks like this:

1. A developer writes new code in their own separate copy, called a **branch**, instead of editing the finished version directly
2. Before that code is added to the main project, someone else looks it over to catch mistakes — this is called a **code review**
3. Once it looks good, it gets combined (**"merged"**) into the main, working version

> **In one line:** Coding turns the design into real, working software.

### 4. Testing

Before real people use the software, the team needs to check that it actually works and doesn't have serious problems (called "bugs").

There are a few different kinds of testing, each checking something different:

- **Unit testing** — checks one small piece of code by itself
- **Integration testing** — checks that different pieces work correctly together
- **End-to-end testing** — checks that a user can complete a full task from start to finish
- **Performance testing** — checks that the software still works well when many people use it at once
- **Security testing** — checks for ways the software could be broken into or misused

Many teams set up a system that tests the code automatically, every single time a developer makes a change. This is called **CI**, short for **Continuous Integration**:

```
Developer saves new code
        ↓
A testing tool starts automatically
        ↓
The code gets checked
        ↓
If everything passes, it's packaged and ready for the next step
```

> **In one line:** Testing makes sure the software actually works before anyone else sees it.

### 5. Deployment

Deployment means releasing the software so real people can finally use it.

Most teams don't release new changes straight to customers. Instead, software usually moves through a few separate spaces first:

| Space | What happens there |
|---|---|
| **Development** | Developers are actively building and changing things |
| **Testing** | The team checks for mistakes |
| **Staging** | One last check, in a space made to look just like the real thing |
| **Production** | The real version that customers actually use |

Moving the software safely between these spaces is often called **CD**, short for **Continuous Delivery** (or **Deployment**). It just means: once the software passes its tests, it gets moved automatically (or with a single click) closer to being available to real users.

Keeping these spaces separate matters: customers keep using the current, working software, while developers can safely test new changes without breaking anything for anyone.

> **In one line:** Deployment is when the software finally goes live.

### 6. Monitoring

Even after the software goes live, the work isn't over. The team keeps watching it — checking for errors, slow performance, security issues, and how people are actually using it.

If something goes wrong, catching it early means the team can usually fix it before it becomes a bigger problem.

This is also why SDLC is often pictured as a **circle** instead of a straight line: what the team learns from monitoring feeds back into planning the next update — and the whole cycle starts again.

> **In one line:** Monitoring keeps the software healthy after launch.

---

## Two Common Ways Teams Organize These Steps

### Waterfall

`Planning → Design → Coding → Testing → Deployment → Maintenance`

Each step is finished completely before the next one starts — like water flowing downhill, it doesn't flow back up. This works well when the requirements are already clear and aren't likely to change.

### Agile

`Plan → Design → Code → Test → Deliver → Get Feedback → Repeat`

Instead of finishing the whole project before showing anyone, the team builds it in small pieces called **sprints**. After each small piece, they show it to the customer, get feedback, and improve it.

**Simple difference:** Waterfall delivers the whole project at the end. Agile delivers small working pieces along the way, and keeps improving as it goes.

---

## A Few Other Models (Good to Know Later)

Once Waterfall and Agile feel comfortable, you may come across a few other approaches. No need to learn these right away:

- **V-Model** — similar to Waterfall, but pairs each building step with a matching testing step
- **Spiral Model** — repeats the steps multiple times, with extra attention on spotting risks early; used on big, complex projects
- **Iterative Model** — builds the software in repeated rounds, each one adding a bit more, somewhat like Agile but with a simpler structure
