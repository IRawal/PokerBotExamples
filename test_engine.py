import unittest
from unittest.mock import patch
from engine import Player

class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player("TestPlayer", "/path/to/player")

    def tearDown(self):
        self.player.stop()

    def test_build_success(self):
        # Mock the subprocess.run function to return a successful build
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = b"Build successful"
            self.player.build()
            self.assertEqual(self.player.commands, {'build': [], 'run': []})

    def test_build_missing_command(self):
        # Mock the subprocess.run function to return a build with missing command
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = b"Build failed"
            self.player.build()
            self.assertIsNone(self.player.commands)
            self.assertIn("commands.json missing command", self.player.bytes_queue.get().decode())

    def test_build_timeout(self):
        # Mock the subprocess.run function to raise a TimeoutExpired exception
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("Timed out", cmd="build")
            self.player.build()
            self.assertIn("Timed out waiting for", self.player.bytes_queue.get().decode())

    def test_run_success(self):
        # Mock the subprocess.Popen function to return a successful run
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.stdout = b"Bot running"
            self.player.run()
            self.assertIsNotNone(self.player.bot_subprocess)
            self.assertIsNotNone(self.player.socketfile)
            self.assertIn("connected successfully", self.player.bytes_queue.get().decode())

    def test_run_missing_command(self):
        # Mock the subprocess.Popen function to return a run with missing command
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.stdout = b"Run failed"
            self.player.run()
            self.assertIsNone(self.player.bot_subprocess)
            self.assertIsNone(self.player.socketfile)
            self.assertIn("run failed - check \"run\" in commands.json", self.player.bytes_queue.get().decode())

    def test_run_timeout(self):
        # Mock the socket.socket function to raise a socket.timeout exception
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.accept.side_effect = socket.timeout("Timed out")
            self.player.run()
            self.assertIn("Timed out waiting for", self.player.bytes_queue.get().decode())

    def test_stop_socket_closed(self):
        # Mock the socketfile.write function to raise a socket.timeout exception
        self.player.socketfile = Mock()
        self.player.socketfile.write.side_effect = socket.timeout("Timed out")
        self.player.stop()
        self.assertIn("Timed out waiting for", self.player.bytes_queue.get().decode())

    def test_stop_subprocess_timeout(self):
        # Mock the bot_subprocess.communicate function to raise a TimeoutExpired exception
        self.player.bot_subprocess = Mock()
        self.player.bot_subprocess.communicate.side_effect = subprocess.TimeoutExpired("Timed out", cmd="run")
        self.player.stop()
        self.assertIn("Timed out waiting for", self.player.bytes_queue.get().decode())

if __name__ == '__main__':
    unittest.main()