# Team Tovarish Style Guide

This guide reiterates some key points from the [pep-8 python style guide](https://peps.python.org/pep-0008/). The guide as a whole should be followed for code submitted to this repository, however this guide highlights the key points. This summary has been created to serve as a quick reference and to accompany submissions when necessary.

# Naming

There are a lot of different naming styles. It helps to be able to recognize what naming style is being used, independently from what they are used for.

The following naming styles are commonly distinguished:

* ``b`` (single lowercase letter)

* ``B`` (single uppercase letter)

* ``lowercase``

* ``lower_case_with_underscores``

* ``UPPERCASE``

* ``UPPER_CASE_WITH_UNDERSCORES``

* ``CapitalizedWords`` (or ``CapWords``, or ``CamelCase`` -- so named because of the bumpy look of its letters). This is also sometimes known as ``StudlyCaps``.

    Note: When using acronyms in CapWords, capitalize all the letters of the acronym. Thus HTTPServerError is better than HttpServerError.

* ``mixedCase`` (differs from CapitalizedWords by initial lowercase character!)

* ``Capitalized_Words_With_Underscores`` (ugly!)



## Class
Class names should normally use the CapWords convention.

The naming convention for functions may be used instead in cases where the interface is documented and used primarily as a callable.

Note that there is a separate convention for builtin names: most builtin names are single words (or two words run together), with the CapWords convention used only for exception names and builtin constants.
## Properties/Attributes
### Designing for Inheritance
Always decide whether a class's methods and instance variables (collectively: "attributes") should be public or non-public. If in doubt, choose non-public; it's easier to make it public later than to make a public attribute non-public.

Public attributes are those that you expect unrelated clients of your class to use, with your commitment to avoid backwards incompatible changes. Non-public attributes are those that are not intended to be used by third parties; you make no guarantees that non-public attributes won't change or even be removed.

We don't use the term "private" here, since no attribute is really private in Python (without a generally unnecessary amount of work).

Another category of attributes are those that are part of the "subclass API" (often called "protected" in other languages). Some classes are designed to be inherited from, either to extend or modify aspects of the class's behavior. When designing such a class, take care to make explicit decisions about which attributes are public, which are part of the subclass API, and which are truly only to be used by your base class.

With this in mind, here are the Pythonic guidelines:

* Public attributes should have no leading underscores.

* If your public attribute name collides with a reserved keyword, append a single trailing underscore to your attribute name. This is preferable to an abbreviation or corrupted spelling. (However, notwithstanding this rule, 'cls' is the preferred spelling for any variable or argument which is known to be a class, especially the first argument to a class method.)

    Note 1: See the argument name recommendation above for class methods.

* For simple public data attributes, it is best to expose just the attribute name, without complicated accessor/mutator methods. Keep in mind that Python provides an easy path to future enhancement, should you find that a simple data attribute needs to grow functional behavior. In that case, use properties to hide functional implementation behind simple data attribute access syntax.

    Note 1: Try to keep the functional behavior side-effect free, although side-effects such as caching are generally fine.

    Note 2: Avoid using properties for computationally expensive operations; the attribute notation makes the caller believe that access is (relatively) cheap.

* If your class is intended to be subclassed, and you have attributes that you do not want subclasses to use, consider naming them with double leading underscores and no trailing underscores. This invokes Python's name mangling algorithm, where the name of the class is mangled into the attribute name. This helps avoid attribute name collisions should subclasses inadvertently contain attributes with the same name.

    Note 1: Note that only the simple class name is used in the mangled name, so if a subclass chooses both the same class name and attribute name, you can still get name collisions.

    Note 2: Name mangling can make certain uses, such as debugging and ``__getattr__()``, less convenient. However the name mangling algorithm is well documented and easy to perform manually.

    Note 3: Not everyone likes name mangling. Try to balance the need to avoid accidental name clashes with potential use by advanced callers.


## Function and Variable Names
Function names should be lowercase, with words separated by underscores as necessary to improve readability.

Variable names follow the same convention as function names.

``mixedCase`` is allowed only in contexts where that's already the prevailing style (e.g. threading.py), to retain backwards compatibility.
### Global Variables
The conventions are about the same as those for functions.

Modules that are designed for use via ``from M import *`` should use the ``__all__`` mechanism to prevent exporting globals, or use the older convention of prefixing such globals with an underscore (which you might want to do to indicate these globals are "module non-public").


## Constants
Constants are usually defined on a module level and written in all capital letters with underscores separating words. Examples include ``MAX_OVERFLOW`` and ``TOTAL``.
## Comments and Comment Style
Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!

Comments should be complete sentences. The first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!).

Block comments generally consist of one or more paragraphs built out of complete sentences, with each sentence ending in a period.

You should use one or two spaces after a sentence-ending period in multi-sentence comments, except after the final sentence.

Ensure that your comments are clear and easily understandable to other speakers of the language you are writing in.

### Block Comments
Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code. Each line of a block comment starts with a ```#``` and a single space (unless it is indented text inside the comment).

Paragraphs inside a block comment are separated by a line containing a single ```#```.

### Inline Comments
Use inline comments sparingly.

An inline comment is a comment on the same line as a statement. Inline comments should be separated by at least two spaces from the statement. They should start with a # and a single space.

### Documentation Strings (docstrings)
Write docstrings for all public modules, functions, classes, and methods. Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does. This comment should appear after the ```def``` line.

# Programming Conventions
## Indentation and Brackets
### Indentation
Use 4 spaces per indentation level (set your IDE to use 4 spaces when you hit tab)

### Opening brackets
Opening brackets should be on the same line as the definition for which the bracket is encapsulating.

### Closing brackets
The closing brace/bracket/parenthesis on multiline constructs may either line up under the first non-whitespace character of the last line of list, as in:

    my_list = [
        1, 2, 3,
        4, 5, 6,
        ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
        )
or it may be lined up under the first character of the line that starts the multiline construct, as in:

    my_list = [
        1, 2, 3,
        4, 5, 6,
    ]
    result = some_function_that_takes_arguments(
        'a', 'b', 'c',
        'd', 'e', 'f',
    )



## Exception Handling
### Exception Names
Because exceptions should be classes, the class naming convention applies here. However, you should use the suffix "Error" on your exception names (if the exception actually is an error).


All exceptions thrown should be logged to the global exception service.