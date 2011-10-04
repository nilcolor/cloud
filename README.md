Why?
===
I like an idea of [cloudapp][1] by [Zach Holman][2]. But I don't want to use `gem` and `ruby`.
No, I do like Ruby. This is cool language and I'll plan to learn it and use it.
But for now - I'm Pythonist. So I do my version of `cloudapp` but name it simply
`cloud`

How?
===
You need to install [Python wrapper][3] of CloudApp API. Next:

* `git clone https://github.com/nilcolor/cloud.git`
* `cd cloud`
* `python cloud.py`

Now you have basic `~/.cloud` settings file which you have to edit. After that
you can make this file executable and symlink it somewhere in the `$PATH`

To be able to run it like normal command you can do something like this:

    # imagine we are still in cloud folder...
    $ chmod +x cloud.py && ln -s `pwd`/cloud.py /usr/local/bin/cloud
    # where `/usr/local/bin/cloud` is something from your $PATH

Now you can do `cloud img1.png foto2.jpg video3.mp4` and get direct links in your
clipboard.  
Oh! If you like to have normal cl.ly link (not directly to files) - you can
change `mode` value to `view` in your `~/.cloud` file.

[1]: https://github.com/holman/dotfiles/blob/master/bin/cloudapp
[2]: http://zachholman.com
[3]: https://github.com/originell/pycloudapp
