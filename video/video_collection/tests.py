from django.test import TestCase
from django.urls import reverse
from .models import Video
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# Create your tests here.


invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?wah=wario',
            'https://www.youtube.com/watch/somethingelse?v=2134235',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch?v=',
            'https://github.com',
            'https://minneapolis.edu'
            'https://minneapolis.edu?v=2345dsfs',
            'hhhhhhttps://www.youtube.com/watch?v=234525',
            '234235',
            'wgsdgwsef',

        ]

class TestHomePageMessage(TestCase):
    def test_app_title_message_shown_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Retro Tech Videos')


class TestAddVideos(TestCase):
    def test_add_valid_video(self):
        valid_video = {
            'name':'retro gaming',
            'url':'https://www.youtube.com/watch?v=mWEE2RJj3YI',
            'notes':'Win98 on a modern pc? nice...'
        }
        url = reverse('add_video')

        response = self.client.post(url, data=valid_video,follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        self.assertContains(response, 'retro gaming')
        self.assertContains(response, 'https://www.youtube.com/watch?v=mWEE2RJj3YI')
        self.assertContains(response, 'Win98 on a modern pc? nice...')
        video_count = Video.objects.count()
        self.assertEqual(1, video_count)

        video = Video.objects.first()
        self.assertEqual(video.name, 'retro gaming' )
        self.assertEqual(video.url, 'https://www.youtube.com/watch?v=mWEE2RJj3YI')
        self.assertEqual(video.notes, 'Win98 on a modern pc? nice...')
        self.assertEqual(video.youtube_id, 'mWEE2RJj3YI')
        
    
    def test_add_video_invalid_url_not_added(self):
        for invalid_url in invalid_video_urls:
            new_video = {
                'name' : 'example',
                'url' : invalid_url,
                'notes' :'example notes'
            }
            url = reverse('add_video')
            response = self.client.post(url, data=new_video)

            self.assertTemplateNotUsed('video_collection/add.html')
            messages = response.context['messages']
            message_texts = [message.message for message in messages]
            self.assertIn('Invalid Youtube URL', message_texts)
            self.assertIn('Please check data entered!', message_texts)
            video_count = Video.objects.count()
            self.assertEqual(video_count, 0)

class TestVideoList(TestCase):
    
    def test_all_videos_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='ABC', notes='example note', url='https://www.youtube.com/watch?v=1234')
        v2 = Video.objects.create(name='aaa', notes='example note', url='https://www.youtube.com/watch?v=5678')
        v3 = Video.objects.create(name='XYS', notes='example note', url='https://www.youtube.com/watch?v=9012')
        v4 = Video.objects.create(name='lmn', notes='example note', url='https://www.youtube.com/watch?v=3456')

        expected_order = [ v2, v1, v4, v3]
        url = reverse('video_list')
        response = self.client.get(url)

        videos_in_template = list(response.context['videos'])
        self.assertEqual(videos_in_template, expected_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.get(url)
        self.assertContains(response, 'No videos!')
        self.assertEqual(0, len(response.context['videos']))
    
    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='ABC', notes='example note', url='https://www.youtube.com/watch?v=1234')

        url = reverse('video_list')
        response = self.client.get(url)

        self.assertContains(response, '1 video')
        self.assertNotContains(response, '1 videos')

    def test_video_number_message_two_videos(self):
            v1 = Video.objects.create(name='ABC', notes='example note', url='https://www.youtube.com/watch?v=1234')
            v2 = Video.objects.create(name='aaa', notes='example note', url='https://www.youtube.com/watch?v=5678')

            url = reverse('video_list')
            response = self.client.get(url)

            self.assertContains(response, '2 videos')


class TestVideoSearch(TestCase):
    pass


class TestVideoModel(TestCase):
    def test_invalid_url_raises_validation_error(self):
        
        for invalid_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_url, notes='example notes')

        self.assertEqual(0, Video.objects.count())
                
    
    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='ABC', notes='example note', url='https://www.youtube.com/watch?v=1234')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='ABC', notes='example note', url='https://www.youtube.com/watch?v=1234')
