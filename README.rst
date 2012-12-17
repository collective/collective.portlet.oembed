Introduction
============

This addon add a portlet which let you use the power of oembed_. The portlet
wait for an URL (required), maxwidth&maxheight (optional) and some display
related options (same as static portlet)

This addon use collective.oembed_ oembed consumer so supported services are
the same.

portlet add/edit form
=====================

* header (TEXT)
* remote_url (URI)
* maxwidth (INT)
* maxheight (INT)
* omit_boder (BOOL)
* footer (TEXT)
* more_url (URI)

Extra feature: Use jquery oembedall for rendering
=================================================

This addon use by default collective.oembed to render the portlet.
It means HTML code is generated server side.
This can be achieved using javascript.

You can install collective.js.oembedall and set the 
'collective.portlet.oebmed.rendering' configuration registry's record to
'collective.js.oembedall'

Credits
=======

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact Makina Corpus <mailto:python@makina-corpus.org>`_


People
------

* JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
.. _oembed: http://oembed.com
.. _collective.oembed: http://pypi.python.org/pypi/collective.oembed
