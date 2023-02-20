from django.db import models
from guardian.shortcuts import assign_perm
from rest_framework.exceptions import PermissionDenied


class WhishListManager(models.Manager):
    def create(self, user, products):
        wishlist = self.create(user=user, products=products)
        wishlist.save()
        assign_perm('change_wishlist', user, wishlist)
        return wishlist

    def edit_wishlist(self, wishlist_id, user):
        wishlist = self.get(id=wishlist_id)
        if user.has_perm('change_wishlist', wishlist):
            wishlist.save()
            return wishlist
        else:
            raise PermissionDenied
