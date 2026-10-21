# Initial Architectural Assessment

The code currently:

- Prompts the user to select from the list of valid countries
- Prints and saves the total cumulative hours of that selected country
- Summarises the data in terms of Short, Standard, and Long EVAs
- Plots cumulative EVA duration over time

There is only one module that performs all functionality.

There is a single loop that performs multiple, unrelated actions
(classifying duration types, appending to a list for plotting)

Dependencies are hard to reason about, as there are no explicit dependencies,
inheritance, or compositions. Dependencies will be implicit and must be discovered
through reading the code.

Almost all functionality is difficult to test. The file name is hard-coded,
category cutoffs are arbitrary, nothing is returned - outputs are printed or
saved as files - and user input is required.
