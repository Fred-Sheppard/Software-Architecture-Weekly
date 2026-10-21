# New Functionality

When implementing the new functionality, the updated architecture made the
changes much easier to introduce. The commit consists almost entire of lines
added - very few lines are changed or removed. The only major update is to
a single function in analysis, and this is simply extracting functionality
to a common helper, reducing duplication. With the old architecture, this change
would have been significantly more difficult to implement while retaining old
functionality.
