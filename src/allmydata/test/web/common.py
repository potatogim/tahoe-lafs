
import re

unknown_rwcap = u"lafs://from_the_future_rw_\u263A".encode('utf-8')
unknown_rocap = u"ro.lafs://readonly_from_the_future_ro_\u263A".encode('utf-8')
unknown_immcap = u"imm.lafs://immutable_from_the_future_imm_\u263A".encode('utf-8')

FAVICON_MARKUP = '<link href="/icon.png" rel="shortcut icon" />'


def assert_soup_has_favicon(testcase, soup):
    """
    Using a ``TestCase`` object ``testcase``, assert that the passed in
    ``BeautifulSoup`` object ``soup`` contains the tahoe favicon link.
    """
    links = soup.find_all(u'link', rel=u'shortcut icon')
    testcase.assert_(
        any(t[u'href'] == u'/icon.png' for t in links), soup)


def assert_soup_has_tag_with_attributes(testcase, soup, tag_name, attrs):
    """
    Using a ``TestCase`` object ``testcase``, assert that the passed
    in ``BeatufulSoup`` object ``soup`` contains a tag ``tag_name``
    (unicode) which has all the attributes in ``attrs`` (dict).
    """
    tags = soup.find_all(tag_name)
    for tag in tags:
        if all(v in tag.attrs.get(k, []) for k, v in attrs.items()):
            return  # we found every attr in this tag; done
    # seems like exceptions can't support unicode text in python2??
    testcase.fail(
        u"No <{}> tags contain attributes: {}".format(tag_name, attrs).encode("utf8")
    )


def assert_soup_has_tag_with_attributes_and_content(testcase, soup, tag_name, content, attrs):
    """
    Using a ``TestCase`` object ``testcase``, assert that the passed
    in ``BeatufulSoup`` object ``soup`` contains a tag ``tag_name``
    (unicode) which has all the attributes in ``attrs`` (dict) and
    contains the string ``content`` (unicode).
    """
    assert_soup_has_tag_with_attributes(testcase, soup, tag_name, attrs)
    assert_soup_has_tag_with_content(testcase, soup, tag_name, content)


def assert_soup_has_tag_with_content(testcase, soup, tag_name, content):
    """
    Using a ``TestCase`` object ``testcase``, assert that the passed
    in ``BeatufulSoup`` object ``soup`` contains a tag ``tag_name``
    (unicode) which contains the string ``content`` (unicode).
    """
    tags = soup.find_all(tag_name)
    for tag in tags:
        if content in tag.contents:
            return
        # make this a "fuzzy" option?
        for c in tag.contents:
            if content in c:
                return
    # seems like exceptions can't support unicode text in python2??
    testcase.fail(
        u"No <{}> tag contains the text '{}'".format(tag_name, content).encode('utf8')
    )


def assert_soup_has_text(testcase, soup, text):
    """
    Using a ``TestCase`` object ``testcase``, assert that the passed in
    ``BeautifulSoup`` object ``soup`` contains the passed in ``text`` anywhere
    as a text node.
    """
    testcase.assert_(
        soup.find_all(string=re.compile(re.escape(text))),
        soup)
