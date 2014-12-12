Dhall - Sign/Verify files
=========================

Inspired by signify

Requirements
-------------

 * Python 2.X (tested with 2.7)
 * ed25519==1.3

Installation
-------------

Either clone locally by running:

```sh
git clone https://github.com/fim/dhall
```

and then install if necessary:

```sh
python setup.py build
python setup.py install
```

Or simply run:

```sh
pip install https://github.com/fim/dhall/tarball/master
```

Usage
-----

Generate a key pair:

```sh
(dhall)$ dhall generate -o /tmp/dhall_key
Generating signing key /tmp/dhall_key
Generating verifying key /tmp/dhall_key.pub
```

Sign a file

```sh
(dhall)$ echo asdf > /tmp/msg
(dhall)$ dhall sign -k /tmp/dhall_key /tmp/msg
Signing file /tmp/msg
Signature: G3zdWmA43TCvuYp6qFqSCaJ/0Nb5wjoW3Rm2tyxNydH+mHt4NOswbybcWmGHwgZTMIdzauLHuufvGAgCuzuFCQ
```

Verify using the public key

```sh
(dhall)$ dhall verify -k /tmp/dhall_key.pub /tmp/msg
Verifying file /tmp/msg
Signature is good
```
