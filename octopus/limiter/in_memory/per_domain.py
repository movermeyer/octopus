#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict


class Limiter(object):
    def __init__(self, *domains):
        self.domains = domains
        self.domain_count = defaultdict(int)

    def get_domain_from_url(self, url):
        for domain in self.domains:
            for key in domain.keys():
                if url.startswith(key):
                    return key
        return None

    def get_domain_limit(self, url):
        for domain in self.domains:
            for key in domain.keys():
                if url.startswith(key):
                    return domain[key]
        return 0

    def acquire(self, url):
        domain = self.get_domain_from_url(url)
        if domain is None:
            logging.info('Tried to acquire lock to a domain that was not specified in the limiter (%s).' % url)
            return True

        limit = self.get_domain_limit(url)

        if self.domain_count[domain] < limit:
            self.domain_count[domain] += 1
            return True

        return False

    def release(self, url):
        domain = self.get_domain_from_url(url)
        if domain is None:
            logging.info('Tried to release lock to a domain that was not specified in the limiter (%s).' % url)
            return

        self.domain_count[domain] -= 1