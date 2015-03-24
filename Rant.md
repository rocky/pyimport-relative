# Why this package? #

What I want is Ruby's _require\_relative_ function. Alas whenever I say that people tell me well of course this has been around since Python 2.6 and is called "relative import". And then they say: Oh, but by the way I don't use that.

And that to me is already a red flag that something is fishy. It is used a lot in the Ruby community.

So I find I have to back up and describe why I want this.

# Reduced development loop cycle #

The overarching concern is reducing time in the development cycle. I want to run code from the source tree without having to install it. _distutils_ creates a _build_ directory, and while it may be necessary in general, it is unnecessary where I have pure Python code. It adds extra time and an additional source of confusion and error.

When I say I want to run from the source tree I really mean the source tree, not an "uninstalled" copy of it in my user filesystem.

Related to this is that I think these system paths are evil. They are long and complicated, fragile, and pose a security risk. So I also want more simple control over where stuff gets loaded.

# Internal versus External Loading #

This leads use to  _internal_ versus _external_ module loading. I have programs that are made up of many sub-modules. A sub-module can be like a top-level module and may someday be one, but at present it isn't. Instead it is always distributed with the package.

Linking parts of submodules inside an overall package should not be subjected to a path search. I _know_ where the package should be. And if it is not there, please I don't want to use some other thing that may be around. This also makes sure when I say I want to run out of the source tree, _I really mean I get all of the code from there that I can, not from an installed version_.

# So what's wrong with Python's relative imports? #

In short, I've never been able to get them to work. If someone can look at the [pydbgr](https://code.google.com/p/pydbgr/) project and get that code to work keeping within my development cycle goals, I'd love to get rid them.

So lastly what are the development cycle goals

# Development cycle goals #

This is what I need when I develop code:

  * Run code from source tree without having to run a "build" or "install" step
  * Be able to run submodules or any file in the filesystem independently. Each submodule is responsible to pull in whatever it needs. But it does it in a relative way. It might not need to know what it's top-level install name is or how it fits into the higher level hierarchy.