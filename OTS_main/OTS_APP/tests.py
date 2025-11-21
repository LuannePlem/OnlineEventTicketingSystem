from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .models import *
from datetime import datetime, date, time, timedelta
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from OTS_APP import views

"""
Testing document for Online Event Ticket Booking System

Tests:
1. User Registration and Authentication
2. Admin Registration and Authentication
3. Event Models 
4. Testing views

"""
# ==========================================================================
# 1. User Registration & Authetication Tests
# ==========================
User = get_user_model()

class UserModelTests(TestCase):

    def test_user_creation_success(self):
        """User is created successfully with all required fields."""
        user = User.objects.create_user(
            username="testuser",
            password="password123",
            age=25,
            user_type="user"
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.age, 25)
        self.assertEqual(user.user_type, "user")

    def test_default_user_type_is_user(self):
        """Check that default user_type is 'user'."""
        user = User.objects.create_user(
            username="defaulttype",
            password="password123",
            age=30
        )
        self.assertEqual(user.user_type, "user")

    def test_invalid_user_type_raises_error(self):
        """Invalid user_type should raise ValidationError."""
        user = User(
            username="badtype",
            password="password123",
            age=22,
            user_type="invalid_role"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_age_required(self):
        """User must have an age value."""
        user = User(
            username="noage",
            password="password123",
            user_type="user"
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_string_representation(self):
        """__str__ returns username."""
        user = User.objects.create_user(
            username="stringtest",
            password="password123",
            age=40,
        )
        self.assertEqual(str(user), "stringtest")

    def test_user_authentication(self):
        """Ensure custom User works with Django auth."""
        user = User.objects.create_user(
            username="authuser",
            password="securepass",
            age=28
        )
        self.assertTrue(user.check_password("securepass"))

    def test_manager_type_creation(self):
        """User can be created with user_type='manager'."""
        user = User.objects.create_user(
            username="manager1",
            password="password123",
            age=35,
            user_type="manager"
        )
        self.assertEqual(user.user_type, "manager")

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)  # redirect to home

    def test_login_invalid_username(self):
        response = self.client.post(reverse("login"), {
            "username": "wrong",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Invalid Username")

# ===========================================================================
# 2. Admin Registration & Authentication Tests
# =============================================
class ManagerModelTests(TestCase):

    def test_manager_creation(self):
        manager = Manager.objects.create_user(
            username="manager1",
            password="testpass123",
            age=30,
            user_type="manager"
        )

        # Check instance
        self.assertIsInstance(manager, Manager)

        # Check inherited attributes
        self.assertEqual(manager.username, "manager1")
        self.assertTrue(manager.check_password("testpass123"))

        # Check default manager fields
        self.assertEqual(manager.total_tickets_sold, 0)
        self.assertEqual(manager.num_current_events, 0)
        self.assertEqual(manager.num_past_events, 0)
        self.assertEqual(manager.total_income, 0.0)

    def test_manager_login(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)  # redirect to home

    def test_manager_string_representation(self):
        manager = Manager.objects.create_user(
            username="bosslady",
            password="password123",
            age=28,
            user_type="manager"
        )

        self.assertEqual(str(manager), "Manager: bosslady")

        def test_wrong_password_fails(self):
            """Manager login should fail with wrong password."""
            manager = User.objects.create_user(
                username="manager2",
                password="correctpass",
                age=38,
                user_type="manager"
            )

            login_successful = self.client.login(
                username="manager2",
                password="wrongpass"
            )

            self.assertFalse(login_successful)

# =============================================================================
# 3.1 Event Models
# =============================
class EventModelTests(TestCase):

    def test_event_str(self):
        event = Event.objects.create(
            event_title="Test Event",
            event_subtitle="Sub",
            event_date=date(2025, 1, 1),
            event_time=time(12, 0),
            event_price=10.0,
            event_location="Test Hall",
            available_seats=50
        )
        self.assertEqual(str(event), "Test Event (2025-01-01)")

    def test_isDatePassed_future_event(self):
        """Event in the future → should return False"""
        tomorrow = datetime.now() + timedelta(days=1)

        event = Event.objects.create(
            event_title="Future Event",
            event_subtitle="Sub",
            event_date=tomorrow.date(),
            event_time=tomorrow.time(),
            event_price=20.0,
            event_location="Future Hall",
            available_seats=100
        )

        self.assertFalse(event.isDatePassed())

    def test_isDatePassed_past_event(self):
        """Event in the past → should return True"""
        yesterday = datetime.now() - timedelta(days=1)

        event = Event.objects.create(
            event_title="Past Event",
            event_subtitle="Sub",
            event_date=yesterday.date(),
            event_time=yesterday.time(),
            event_price=20.0,
            event_location="Past Hall",
            available_seats=100
        )

        self.assertTrue(event.isDatePassed())

    def test_isDatePassed_same_day_future_time(self):
        """Today but later time → should return False"""
        now = datetime.now()
        later_time = (now + timedelta(hours=1)).time()

        event = Event.objects.create(
            event_title="Later Today",
            event_subtitle="Sub",
            event_date=now.date(),
            event_time=later_time,
            event_price=15.0,
            event_location="Main Hall",
            available_seats=30
        )

        self.assertFalse(event.isDatePassed())

    def test_isDatePassed_same_day_past_time(self):
        """Today but earlier time → should return True"""
        now = datetime.now()
        earlier_time = (now - timedelta(hours=1)).time()

        event = Event.objects.create(
            event_title="Earlier Today",
            event_subtitle="Sub",
            event_date=now.date(),
            event_time=earlier_time,
            event_price=15.0,
            event_location="Main Hall",
            available_seats=30
        )

        self.assertTrue(event.isDatePassed())

# ==========================================================================
# 3.2 Testing Bookings 
# ====================

class BookingModelTests(TestCase):

    def setUp(self):
        """Common setup for all booking tests."""
        self.user = User.objects.create_user(username="john", password="123", age=25)
        self.event = Event.objects.create(
            event_title="Concert",
            event_subtitle="Live Music",
            event_date=date(2025, 1, 1),
            event_time=time(18, 0),
            event_price=50.0,
            event_location="City Hall",
            available_seats=100
        )

    def test_booking_str(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            seats_booked=2
        )

        expected = "john booked 2 seats for Concert"
        self.assertEqual(str(booking), expected)

    def test_valid_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            seats_booked=3
        )

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.event, self.event)
        self.assertEqual(booking.seats_booked, 3)

    def test_unique_together_user_event(self):
        # reuse self.user created in setUp
        event = Event.objects.create(
            event_title="Test Event",
            event_subtitle="Sub",
            event_date=date(2025, 1, 1),
            event_time=time(10, 0),
            event_price=10.0,
            event_location="Location",
            available_seats=100,
            creator=self.user
        )

        b = Booking(user=self.user, event=self.event, seats_booked=1)
        b.save()

        duplicate = Booking(user=self.user, event=self.event, seats_booked=2)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate.save()

    def test_booking_deleted_when_user_deleted(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            seats_booked=1
        )

        self.user.delete()

        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_deleted_when_event_deleted(self):
        booking = Booking.objects.create(
            user=self.user,
            event=self.event,
            seats_booked=1
        )

        self.event.delete()

        self.assertEqual(Booking.objects.count(), 0)

# ===========================================================================
# 4. Test views
# ================================
class AuthViewTests(TestCase):

    def setUp(self):
        self.password = "testpass1223"
        self.user = User.objects.create_user(
            username="john",
            password=self.password,
            age=21,
            user_type="user"
        )

    # ----------------------
    # LOGIN VIEW TESTS
    # ----------------------

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "username": "john",
            "password": self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")     # redirect home
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_invalid_username(self):
        response = self.client.post(reverse("login"), {
            "username": "not_user",
            "password": "abc123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

    def test_login_invalid_password(self):
        response = self.client.post(reverse("login"), {
            "username": "john",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

    # ----------------------
    # REGISTER VIEW TESTS
    # ----------------------

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register_new_user(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "username": "alice",
            "password": "mypassword",
            "age": "22",
            "user_type": "user"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

        # user actually exists
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_register_duplicate_username(self):
        response = self.client.post(reverse("register"), {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john2@example.com",
            "username": "john",  # already exists
            "password": "123",
            "age": "22",
            "user_type": "user"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/register/")

    # ----------------------
    # HOME VIEW TEST
    # ----------------------

    def test_home_view_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

# ===========================================================================
# 5. Testing URLS
# ================================
class URLTests(TestCase):

    def setUp(self):
        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser",
            password="12345",
            age=20
        )

        # Create event for parameterized URL tests
        self.event = Event.objects.create(
            event_title="Test Event",
            event_subtitle="Sub",
            event_date=date.today(),
            event_time=time(12, 0),
            event_price=10,
            event_location="Here",
            available_seats=100,
            creator=self.user
        )

    # -------------------------------------------------
    # BASIC PUBLIC URLS (no login required)
    # -------------------------------------------------
    def test_home_url_resolves(self):
        self.assertEqual(resolve("/").func, views.home)

    def test_home_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_upcoming_events_url(self):
        # create user
        user = User.objects.create_user(username="jimmie", password="jimmie22", age=22)

        # login first
        self.client.login(username="jimmie", password="jimmie22")

        # access page as authenticated user
        response = self.client.get(reverse("upcoming"))

        # now this should be 200
        self.assertEqual(response.status_code, 200)


    def test_current_events_url(self):
        # Create user
        user = User.objects.create_user(username="james", password="james3", age=22)

        # Log them in
        self.client.login(username="james", password="james3")

        # Request URL
        response = self.client.get(reverse("current"))

        # Should now be OK
        self.assertEqual(response.status_code, 200)


    def test_individual_event_url(self):
        response = self.client.get(reverse("individualEvent"))
        self.assertEqual(response.status_code, 200)

    # -------------------------------------------------
    # URLS THAT REQUIRE LOGIN
    # -------------------------------------------------
    def test_create_event_requires_login(self):
        response = self.client.get(reverse("createEvent"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_event_requires_login(self):
        response = self.client.get(reverse("editEvent", args=[self.event.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_event_requires_login(self):
        response = self.client.get(reverse("deleteEvent", args=[self.event.id]))
        self.assertEqual(response.status_code, 302)

    # -------------------------------------------------
    # LOGGED-IN USER ACCESS
    # -------------------------------------------------
    def test_logged_in_user_can_access_edit_event(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("editEvent", args=[self.event.id]))
        self.assertIn(response.status_code, [200, 403])

    def test_logged_in_user_can_access_delete_event(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("deleteEvent", args=[self.event.id]))
        self.assertIn(response.status_code, [200, 403])