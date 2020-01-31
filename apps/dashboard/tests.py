from django.test import TestCase

from apps.users.models import CustomUser
from .models import Organization, ClubCategory


class OrganizationModelTests(TestCase):

    def test_get_main_club_categories(self):
        owner = CustomUser.objects.create_user('test@test.pl', 'SuperStrongP455')
        organization = Organization.objects.create(owner=owner, name='organization name')
        category_1 = ClubCategory.objects.create(organization=organization, name='category 1')
        category_2 = ClubCategory.objects.create(organization=organization, name='category 2')
        category_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-1', parent=category_2)
        category_2_2 = ClubCategory.objects.create(organization=organization, name='category 2-2', parent=category_2)
        category_2_3 = ClubCategory.objects.create(organization=organization, name='category 2-3', parent=category_2)
        category_2_3_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-1', parent=category_2_3)
        category_2_3_2 = ClubCategory.objects.create(organization=organization, name='category 2-3-2', parent=category_2_3)
        category_2_3_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-2-1', parent=category_2_3_2)
        category_2_3_3 = ClubCategory.objects.create(organization=organization, name='category 2-3-3', parent=category_2_3)
        category_2_4 = ClubCategory.objects.create(organization=organization, name='category 2-4', parent=category_2)
        category_2_4_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-1', parent=category_2_4)
        category_2_4_2 = ClubCategory.objects.create(organization=organization, name='category 2-4-2', parent=category_2_4)
        category_2_4_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1', parent=category_2_4_2)
        category_2_4_2_1_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1-1', parent=category_2_4_2_1)
        category_2_4_3 = ClubCategory.objects.create(organization=organization, name='category 2-4-3', parent=category_2_4)
        category_2_5 = ClubCategory.objects.create(organization=organization, name='category 2-5', parent=category_2)
        category_3 = ClubCategory.objects.create(organization=organization, name='category 3')
        category_3_1 = ClubCategory.objects.create(organization=organization, name='category 3-1', parent=category_3)
        category_3_2 = ClubCategory.objects.create(organization=organization, name='category 3-2', parent=category_3)
        category_3_3 = ClubCategory.objects.create(organization=organization, name='category 3-3', parent=category_3)
        category_4 = ClubCategory.objects.create(organization=organization, name='category 4')
        category_4_1 = ClubCategory.objects.create(organization=organization, name='category 4-1', parent=category_4)
        category_4_2 = ClubCategory.objects.create(organization=organization, name='category 4-2', parent=category_4)

        self.assertListEqual(
            list(organization.get_main_club_categories()),
            [category_1, category_2, category_3, category_4],
        )


class ClubCategoryModelTests(TestCase):

    def test_distance_to_root(self):
        owner = CustomUser.objects.create_user('test@test.pl', 'SuperStrongP455')
        organization = Organization.objects.create(owner=owner, name='organization name')
        category_1 = ClubCategory.objects.create(organization=organization, name='category 1')
        category_2 = ClubCategory.objects.create(organization=organization, name='category 2')
        category_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-1', parent=category_2)
        category_2_2 = ClubCategory.objects.create(organization=organization, name='category 2-2', parent=category_2)
        category_2_3 = ClubCategory.objects.create(organization=organization, name='category 2-3', parent=category_2)
        category_2_3_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-1', parent=category_2_3)
        category_2_3_2 = ClubCategory.objects.create(organization=organization, name='category 2-3-2', parent=category_2_3)
        category_2_3_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-2-1', parent=category_2_3_2)
        category_2_3_3 = ClubCategory.objects.create(organization=organization, name='category 2-3-3', parent=category_2_3)
        category_2_4 = ClubCategory.objects.create(organization=organization, name='category 2-4', parent=category_2)
        category_2_4_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-1', parent=category_2_4)
        category_2_4_2 = ClubCategory.objects.create(organization=organization, name='category 2-4-2', parent=category_2_4)
        category_2_4_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1', parent=category_2_4_2)
        category_2_4_2_1_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1-1', parent=category_2_4_2_1)
        category_2_4_3 = ClubCategory.objects.create(organization=organization, name='category 2-4-3', parent=category_2_4)
        category_2_5 = ClubCategory.objects.create(organization=organization, name='category 2-5', parent=category_2)
        category_3 = ClubCategory.objects.create(organization=organization, name='category 3')
        category_3_1 = ClubCategory.objects.create(organization=organization, name='category 3-1', parent=category_3)
        category_3_2 = ClubCategory.objects.create(organization=organization, name='category 3-2', parent=category_3)
        category_3_3 = ClubCategory.objects.create(organization=organization, name='category 3-3', parent=category_3)
        category_4 = ClubCategory.objects.create(organization=organization, name='category 4')
        category_4_1 = ClubCategory.objects.create(organization=organization, name='category 4-1', parent=category_4)
        category_4_2 = ClubCategory.objects.create(organization=organization, name='category 4-2', parent=category_4)

        self.assertEqual(category_1.distance_to_root(), 0)
        self.assertEqual(category_2.distance_to_root(), 0)
        self.assertEqual(category_2_1.distance_to_root(), 1)
        self.assertEqual(category_2_2.distance_to_root(), 1)
        self.assertEqual(category_2_3.distance_to_root(), 1)
        self.assertEqual(category_2_3_1.distance_to_root(), 2)
        self.assertEqual(category_2_3_2.distance_to_root(), 2)
        self.assertEqual(category_2_3_2_1.distance_to_root(), 3)
        self.assertEqual(category_2_3_3.distance_to_root(), 2)
        self.assertEqual(category_2_4.distance_to_root(), 1)
        self.assertEqual(category_2_4_1.distance_to_root(), 2)
        self.assertEqual(category_2_4_2.distance_to_root(), 2)
        self.assertEqual(category_2_4_2_1.distance_to_root(), 3)
        self.assertEqual(category_2_4_2_1_1.distance_to_root(), 4)
        self.assertEqual(category_2_4_3.distance_to_root(), 2)
        self.assertEqual(category_2_5.distance_to_root(), 1)
        self.assertEqual(category_3.distance_to_root(), 0)
        self.assertEqual(category_3_1.distance_to_root(), 1)
        self.assertEqual(category_3_2.distance_to_root(), 1)
        self.assertEqual(category_3_3.distance_to_root(), 1)
        self.assertEqual(category_4.distance_to_root(), 0)
        self.assertEqual(category_4_1.distance_to_root(), 1)
        self.assertEqual(category_4_2.distance_to_root(), 1)

    def test_distance_to_farthest_leaf(self):
        owner = CustomUser.objects.create_user('test@test.pl', 'SuperStrongP455')
        organization = Organization.objects.create(owner=owner, name='organization name')
        category_1 = ClubCategory.objects.create(organization=organization, name='category 1')
        category_2 = ClubCategory.objects.create(organization=organization, name='category 2')
        category_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-1', parent=category_2)
        category_2_2 = ClubCategory.objects.create(organization=organization, name='category 2-2', parent=category_2)
        category_2_3 = ClubCategory.objects.create(organization=organization, name='category 2-3', parent=category_2)
        category_2_3_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-1', parent=category_2_3)
        category_2_3_2 = ClubCategory.objects.create(organization=organization, name='category 2-3-2', parent=category_2_3)
        category_2_3_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-2-1', parent=category_2_3_2)
        category_2_3_3 = ClubCategory.objects.create(organization=organization, name='category 2-3-3', parent=category_2_3)
        category_2_4 = ClubCategory.objects.create(organization=organization, name='category 2-4', parent=category_2)
        category_2_4_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-1', parent=category_2_4)
        category_2_4_2 = ClubCategory.objects.create(organization=organization, name='category 2-4-2', parent=category_2_4)
        category_2_4_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1', parent=category_2_4_2)
        category_2_4_2_1_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1-1', parent=category_2_4_2_1)
        category_2_4_3 = ClubCategory.objects.create(organization=organization, name='category 2-4-3', parent=category_2_4)
        category_2_5 = ClubCategory.objects.create(organization=organization, name='category 2-5', parent=category_2)
        category_3 = ClubCategory.objects.create(organization=organization, name='category 3')
        category_3_1 = ClubCategory.objects.create(organization=organization, name='category 3-1', parent=category_3)
        category_3_2 = ClubCategory.objects.create(organization=organization, name='category 3-2', parent=category_3)
        category_3_3 = ClubCategory.objects.create(organization=organization, name='category 3-3', parent=category_3)
        category_4 = ClubCategory.objects.create(organization=organization, name='category 4')
        category_4_1 = ClubCategory.objects.create(organization=organization, name='category 4-1', parent=category_4)
        category_4_2 = ClubCategory.objects.create(organization=organization, name='category 4-2', parent=category_4)

        self.assertEqual(category_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2.distance_to_farthest_leaf(), 4)
        self.assertEqual(category_2_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_2.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_3.distance_to_farthest_leaf(), 2)
        self.assertEqual(category_2_3_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_3_2.distance_to_farthest_leaf(), 1)
        self.assertEqual(category_2_3_2_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_3_3.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_4.distance_to_farthest_leaf(), 3)
        self.assertEqual(category_2_4_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_4_2.distance_to_farthest_leaf(), 2)
        self.assertEqual(category_2_4_2_1.distance_to_farthest_leaf(), 1)
        self.assertEqual(category_2_4_2_1_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_4_3.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_2_5.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_3.distance_to_farthest_leaf(), 1)
        self.assertEqual(category_3_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_3_2.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_3_3.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_4.distance_to_farthest_leaf(), 1)
        self.assertEqual(category_4_1.distance_to_farthest_leaf(), 0)
        self.assertEqual(category_4_2.distance_to_farthest_leaf(), 0)

    def test_get_children(self):
        owner = CustomUser.objects.create_user('test@test.pl', 'SuperStrongP455')
        organization = Organization.objects.create(owner=owner, name='organization name')
        category_1 = ClubCategory.objects.create(organization=organization, name='category 1')
        category_2 = ClubCategory.objects.create(organization=organization, name='category 2')
        category_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-1', parent=category_2)
        category_2_2 = ClubCategory.objects.create(organization=organization, name='category 2-2', parent=category_2)
        category_2_3 = ClubCategory.objects.create(organization=organization, name='category 2-3', parent=category_2)
        category_2_3_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-1', parent=category_2_3)
        category_2_3_2 = ClubCategory.objects.create(organization=organization, name='category 2-3-2', parent=category_2_3)
        category_2_3_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-2-1', parent=category_2_3_2)
        category_2_3_3 = ClubCategory.objects.create(organization=organization, name='category 2-3-3', parent=category_2_3)
        category_2_4 = ClubCategory.objects.create(organization=organization, name='category 2-4', parent=category_2)
        category_2_4_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-1', parent=category_2_4)
        category_2_4_2 = ClubCategory.objects.create(organization=organization, name='category 2-4-2', parent=category_2_4)
        category_2_4_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1', parent=category_2_4_2)
        category_2_4_2_1_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1-1', parent=category_2_4_2_1)
        category_2_4_3 = ClubCategory.objects.create(organization=organization, name='category 2-4-3', parent=category_2_4)
        category_2_5 = ClubCategory.objects.create(organization=organization, name='category 2-5', parent=category_2)
        category_3 = ClubCategory.objects.create(organization=organization, name='category 3')
        category_3_1 = ClubCategory.objects.create(organization=organization, name='category 3-1', parent=category_3)
        category_3_2 = ClubCategory.objects.create(organization=organization, name='category 3-2', parent=category_3)
        category_3_3 = ClubCategory.objects.create(organization=organization, name='category 3-3', parent=category_3)
        category_4 = ClubCategory.objects.create(organization=organization, name='category 4')
        category_4_1 = ClubCategory.objects.create(organization=organization, name='category 4-1', parent=category_4)
        category_4_2 = ClubCategory.objects.create(organization=organization, name='category 4-2', parent=category_4)

        self.assertListEqual(
            list(category_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2.get_children()),
            [category_2_1, category_2_2, category_2_3, category_2_4, category_2_5],
        )
        self.assertListEqual(
            list(category_2_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_2.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_3.get_children()),
            [category_2_3_1, category_2_3_2, category_2_3_3],
        )
        self.assertListEqual(
            list(category_2_3_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_3_2.get_children()),
            [category_2_3_2_1],
        )
        self.assertListEqual(
            list(category_2_3_2_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_3_3.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_4.get_children()),
            [category_2_4_1, category_2_4_2, category_2_4_3],
        )
        self.assertListEqual(
            list(category_2_4_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_4_2.get_children()),
            [category_2_4_2_1],
        )
        self.assertListEqual(
            list(category_2_4_2_1.get_children()),
            [category_2_4_2_1_1],
        )
        self.assertListEqual(
            list(category_2_4_2_1_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_4_3.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_2_5.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_3.get_children()),
            [category_3_1, category_3_2, category_3_3],
        )
        self.assertListEqual(
            list(category_3_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_3_2.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_3_3.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_4.get_children()),
            [category_4_1, category_4_2],
        )
        self.assertListEqual(
            list(category_4_1.get_children()),
            [],
        )
        self.assertListEqual(
            list(category_4_2.get_children()),
            [],
        )

    def test_am_i_in_myself(self):
        owner = CustomUser.objects.create_user('test@test.pl', 'SuperStrongP455')
        organization = Organization.objects.create(owner=owner, name='organization name')
        category_1 = ClubCategory.objects.create(organization=organization, name='category 1')
        category_2 = ClubCategory.objects.create(organization=organization, name='category 2')
        category_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-1', parent=category_2)
        category_2_2 = ClubCategory.objects.create(organization=organization, name='category 2-2', parent=category_2)
        category_2_3 = ClubCategory.objects.create(organization=organization, name='category 2-3', parent=category_2)
        category_2_3_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-1', parent=category_2_3)
        category_2_3_2 = ClubCategory.objects.create(organization=organization, name='category 2-3-2', parent=category_2_3)
        category_2_3_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-3-2-1', parent=category_2_3_2)
        category_2_3_3 = ClubCategory.objects.create(organization=organization, name='category 2-3-3', parent=category_2_3)
        category_2_4 = ClubCategory.objects.create(organization=organization, name='category 2-4', parent=category_2)
        category_2_4_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-1', parent=category_2_4)
        category_2_4_2 = ClubCategory.objects.create(organization=organization, name='category 2-4-2', parent=category_2_4)
        category_2_4_2_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1', parent=category_2_4_2)
        category_2_4_2_1_1 = ClubCategory.objects.create(organization=organization, name='category 2-4-2-1-1', parent=category_2_4_2_1)
        category_2_4_3 = ClubCategory.objects.create(organization=organization, name='category 2-4-3', parent=category_2_4)
        category_2_5 = ClubCategory.objects.create(organization=organization, name='category 2-5', parent=category_2)
        category_3 = ClubCategory.objects.create(organization=organization, name='category 3')
        category_3_1 = ClubCategory.objects.create(organization=organization, name='category 3-1', parent=category_3)
        category_3_2 = ClubCategory.objects.create(organization=organization, name='category 3-2', parent=category_3)
        category_3_3 = ClubCategory.objects.create(organization=organization, name='category 3-3', parent=category_3)
        category_4 = ClubCategory.objects.create(organization=organization, name='category 4')
        category_4_1 = ClubCategory.objects.create(organization=organization, name='category 4-1', parent=category_4)
        category_4_2 = ClubCategory.objects.create(organization=organization, name='category 4-2', parent=category_4)

        self.assertTrue(category_1.am_i_in_myself(category_1))
        self.assertTrue(category_2.am_i_in_myself(category_2))
        self.assertTrue(category_2_1.am_i_in_myself(category_2))
        self.assertTrue(category_2_2.am_i_in_myself(category_2))
        self.assertTrue(category_2_3.am_i_in_myself(category_2))
        self.assertTrue(category_2_4_2_1_1.am_i_in_myself(category_2))

        self.assertFalse(category_2_4.am_i_in_myself(category_2_4_2))
