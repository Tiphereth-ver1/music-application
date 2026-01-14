import unittest
from player import Player
from song import Song

class TestPlayer(unittest.TestCase):

    def setUp(self):
        # Initialize player and songs
        self.player = Player()
        self.song1 = Song("beat_it.mp3")
        self.song2 = Song("thriller.mp3")
        self.song3 = Song("billie_jean.mp3")
        self.song4 = Song("this_girl_is_mine.mp3")
        self.songs = [self.song1, self.song2, self.song3, self.song4]

    def test_queue_songs(self):
        self.player.queue_songs(self.songs)
        self.assertEqual(len(self.player.queue), 4)
        self.assertEqual(self.player.queue[0], self.song1)

    def test_next_song(self):
        self.player.queue_songs(self.songs)
        self.player.next_song()
        self.assertEqual(self.player.playing, self.song1)
        self.assertEqual(len(self.player.history), 0)  # first song has no previous history
        self.player.next_song()  # move to next song
        self.assertEqual(self.player.playing, self.song2)
        self.assertEqual(self.player.history[-1], self.song1)  # now song1 is in history


    def test_previous_song(self):
        self.player.queue_songs(self.songs)
        self.player.next_song()
        self.player.next_song()
        self.player.previous_song()
        self.assertEqual(self.player.playing, self.song1)

    def test_shuffle_queue(self):
        self.player.queue_songs(self.songs)
        original_order = list(self.player.queue)
        self.player.shuffle_queue()
        shuffled_order = list(self.player.queue)
        self.assertNotEqual(original_order, shuffled_order)

    def test_remove_song(self):
        self.player.queue_songs(self.songs)
        self.player.remove_song(self.song2)
        self.assertNotIn(self.song2, self.player.queue)
        # Removing a song not in queue
        self.player.remove_song(self.song2)

    def test_insert_song(self):
        self.player.queue_songs([self.song1, self.song3])
        self.player.insert_song(self.song2, 1)
        self.assertEqual(list(self.player.queue)[1], self.song2)

    def test_skip(self):
        self.player.queue_songs(self.songs)
        self.player.skip(2)
        self.assertEqual(self.player.history[-1], self.song2)
        self.assertEqual(len(self.player.queue), 2)
        # skipping more than available
        self.player.skip(5)

    def test_loop_modes(self):
        self.player.queue_songs(self.songs)
        self.player.toggle_loop("single")
        self.assertEqual(self.player.loop_mode, "single")
        self.player.toggle_loop("playlist")
        self.assertEqual(self.player.loop_mode, "playlist")
        self.player.toggle_loop("none")
        self.assertEqual(self.player.loop_mode, "none")
        # Invalid mode
        self.player.toggle_loop("invalid")

if __name__ == "__main__":
    unittest.main()
