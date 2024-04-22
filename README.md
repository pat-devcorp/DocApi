[style_conventions]

https://nimblehq.co/compass/production/postmortem/

- Repository data attributes: Camel Case
- objects class: first letter only
- Util Class: Upper Case
- Flow Class: Lower Case
- Infrastructure: Must have mock basic on type and the specific implementation using a library must have test
- Connection Class: must implement in out decorator
- Function
  - Philosophy: must be verbs, Camel Case, if you can describe the function in 4 blocks split
  - Local Variable in functions: Snake Case
  - decorators: Snake Case
  - reference to a class object: starts with ref_

-States in model: use dates or state machines

export $(cat .env | xargs) 