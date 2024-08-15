# ATRtool

ATRtool is a web tool and companion Python package to manipulate smartcard ATRs. (ATR = Answer-To-Reset)

The web tool is built using Bootstrap and PyScript. Bootstrap was chosen for the UI because of how easy it is to create good-looking and responsive interfaces with minimal effort. PyScript was chosen because I wanted to write the object handling code in Python (due to prior experience), but leave the UI in a browser without having to implement a client-server model.


# How to run

You can serve the project folder with any HTTP server. An internet connection is required for external dependencies of the webpage, but if offline use isrequired, copies of those files can be downloaded and hosted with the project files (this process will be left as an exercise to the reader).
Do keep in mind that it is not possible to simply open the `index.html` file in a web browser directly, as it will not be able to load the Python files, because it is prevented by browser security measures.

If you have Python installed, the easiest way to serve the files would be to run:

```sh
python3 -m http.server
```

and then open <http://localhost:8000> in a browser.


# TODO

- [ ] add protocol-specific parameters
- [ ] add presets
- [ ] write documentation
