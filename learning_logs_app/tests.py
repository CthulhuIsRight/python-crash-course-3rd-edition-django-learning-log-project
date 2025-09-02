from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Topic, Entry

class URLTests(TestCase):
	def setUp(self):
		self.client = Client()
		# Create a user and log in
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.client.login(username='testuser', password='testpass')
		# Create another user
		self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
		# Create a topic for self.user
		self.topic = Topic.objects.create(text='Test Topic', owner=self.user)
		# Create an entry for self.topic
		self.entry = Entry.objects.create(topic=self.topic, text='Test Entry')

	def test_index_url(self):
		response = self.client.get(reverse('learning_logs_app:index'))
		self.assertEqual(response.status_code, 200)

	def test_topics_url(self):
		response = self.client.get(reverse('learning_logs_app:topics'))
		# If login required, expect redirect (302), else 200
		self.assertIn(response.status_code, [200, 302])

	def test_new_topic_url(self):
		response = self.client.get(reverse('learning_logs_app:new_topic'))
		self.assertIn(response.status_code, [200, 302])

	def test_topic_detail_url(self):
		response = self.client.get(reverse('learning_logs_app:topic', args=[self.topic.id]))
		self.assertEqual(response.status_code, 200)

	def test_new_entry_url(self):
		response = self.client.get(reverse('learning_logs_app:new_entry', args=[self.topic.id]))
		self.assertEqual(response.status_code, 200)

	def test_edit_entry_url(self):
		response = self.client.get(reverse('learning_logs_app:edit_entry', args=[self.entry.id]))
		self.assertEqual(response.status_code, 200)

	def test_topic_permission(self):
		# Try to access other user's topic
		other_topic = Topic.objects.create(text='Other Topic', owner=self.other_user)
		response = self.client.get(reverse('learning_logs_app:topic', args=[other_topic.id]))
		self.assertEqual(response.status_code, 404)

	def test_edit_entry_permission(self):
		# Entry for other user's topic
		other_topic = Topic.objects.create(text='Other Topic', owner=self.other_user)
		other_entry = Entry.objects.create(topic=other_topic, text='Other Entry')
		response = self.client.get(reverse('learning_logs_app:edit_entry', args=[other_entry.id]))
		self.assertEqual(response.status_code, 404)

	def test_create_topic_form(self):
		response = self.client.post(reverse('learning_logs_app:new_topic'), {'text': 'New Topic'})
		self.assertEqual(response.status_code, 302)  # Should redirect after creation
		self.assertTrue(Topic.objects.filter(text='New Topic', owner=self.user).exists())

	def test_create_entry_form(self):
		response = self.client.post(reverse('learning_logs_app:new_entry', args=[self.topic.id]), {'text': 'New Entry'})
		self.assertEqual(response.status_code, 302)  # Should redirect after creation
		self.assertTrue(Entry.objects.filter(text='New Entry', topic=self.topic).exists())

	def test_edit_entry_form(self):
		response = self.client.post(reverse('learning_logs_app:edit_entry', args=[self.entry.id]), {'text': 'Edited Entry'})
		self.assertEqual(response.status_code, 302)  # Should redirect after edit
		self.entry.refresh_from_db()
		self.assertEqual(self.entry.text, 'Edited Entry')

	# Add more tests for topic, new_entry, edit_entry if you want to check with specific IDs

# Create your tests here.
