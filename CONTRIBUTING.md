# Guidelines to write a tutorial

Here is some useful information you should take into account when writing a tutorial, in particular
the various Advanced topics.

## Getting started

It is always easier for a reader to have a reference starting point at the beginning of a tutorial.
The Core Training tutorial should give a decent starting point for any advanced topic: the module
contains various models, multiple type of fields, views and actions. It will save you and the
reader time by avoiding the boiler plate of re-creating a business scenario from scratch.

Be clear about the requirements. It might be general knowledge or practical information. Example:

> This tutorial assumes you followed the Core Training.
>
> To do the exercise, fetch the branch `14.0-core` from the repository XXX. It contains
> a basic module we will use as a starting point.

There is no magic recipe to write a tutorial, but here is an idea of what could be done:

1. Write the Table of Contents: list all the concepts you want to cover. This will help you to know
   where to start. Do not try to cover too many concepts: the purpose of a tutorial is to help the
   reader getting a first grasp on a topic, not turn him/her into an expert.
2. Write the solution: before writing any line of text, write the solution. This will give you
   the finish line you want to reach. It will also help you to realize if it is possible to
   easily cover the various concepts.
3. Write the tutorial: now you have the starting and finish points, it is time to write the path
   to join them.

In all cases, keep it 'easy': the purpose of a tutorial is to give a limited quantity of
information but be sure that everything is understood.

## Business need

The first step of the tutorial is to explain what is the business need behind the new topic you are
going to introduce. Write a few words to summarize what we did in the Core Training, then
explain what is missing for the business case. It's important for a reader to understand **why**
he/she is doing something. Example:

> The previous chapter introduced the possibility to add some business logic to our model.
> We can now link buttons to business code. But how can we prevent users from encoding
> incorrect data? For example, in our real estate module, nothing prevents the
> user to set a negative expected price.

Then, give a few words about the solution Odoo provides for the need. Example:

> Odoo provides two ways to set up automatically verified invariants Python constraints and
> SQL constraints.

The reader knows to what business need the topic is useful.

## Technical information

When the context is set, you can introduce the technical solution. Do not hesitate to split it
into relevant sections. In the previous example, the split is obvious: a section is dedicated
to SQL constraints, the other is dedicated to Python constraints.

Start each section by a clear reference to the documentation linked to the topic. Example:

> **Reference**: the documentation related to this topic can be found in `XXX` and `YYY`.

Refrain from 'hiding' links within the text: it makes the reader unaware of what are the important
documents referenced.

Then, give the goal of the section: what is the reader supposed to achieve at the end of the
section? Example:

> **Goal**: at the end of this section:
> - Amounts should be (strictly) positive
> - Property types and tags have a unique name

If possible, add screenshots or short animated gifs for a better visualization of what
is expected. It helps the reader searching by himself for a solution matching the screenshot.

Now that the reader knows where to find extra documentation and what is the purpose of the section,
give the necessary technical information. Do not hesitate to give code snippets or link
to simple examples in the Odoo codebase. It's not always easy to find a good balance between
the necessary information to solve the exercise and being complete. Once again, it might be
better to give an incomplete but useful information rather than an exhaustive list of all the
options which will be forgotten soon after the training.

Try to think it this way: what does the reader already know and what else does he/she need to know
to solve the exercise?

Do not hesitate to split complex sections in various steps. For example, the chapter 
'Interact With Other Modules' splits the invoice creation into 3 exercises:

- override the necessary method and call `super`
- in the override, create an empty invoice
- add the invoice lines to the invoice creation

It gives the reader intermediary points where he/she can make sure to be on the right track.

## Limitations and pitfalls

All technical solution has its limitations and pitfalls. It might be a matter of performance
(e.g. computed fields), maintenance (e.g. custom JS widgets), or... anything.
Be more specific about when to use this solution and when not use it.

## Test and review your tutorial

Ask a colleague for a review of your tutorial: something that might be obvious to you
might not be for someone else.

## Add your solution to this repository

Create a specific branch in this repository with the solution. For the Advanced topics, it is
suggested to create a new branch from `14.0-core` and add a single commit with the solution.
Multiple commits might be tempting (e.g. to show the step-by-step solution), but they are way more
complex to maintain.

In the end, if the exercise was explained clearly, only the final solution should be useful to
the reader.
