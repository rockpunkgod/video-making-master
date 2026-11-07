"""Synthetic reviewer declarations test the gate, never certify actual viewing."""
import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('art_direction', SKILL/'scripts/art_direction.py')
ad = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ad)


class EvidenceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='vad-contract-tests-')
        cls.root = Path(cls.tmp.name)
        cls.video = cls.root/'synthetic.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=64x64:rate=10:duration=1',
                        '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', '-c:v', 'libx264', '-threads', '2',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(cls.video)], check=True)
        cls.brief = ad.read(SKILL/'examples/resonance-brief.json')
        brief = copy.deepcopy(cls.brief)
        brief['format'] = dict(width=64, height=64, fps=10, duration_s=1)
        brief['shots'] = [dict(start=0, end=1, focus='fixture', framing='fixture', movement='fixture', motivation='fixture', sound='fixture')]
        ad.write(cls.root/'brief.json', brief)
        ad.packet(cls.root/'brief.json', cls.video, cls.root/'packet')
        cls.packet = cls.root/'packet/review-packet.json'

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def fixture(self):
        r = ad.read(self.root/'packet/review-template.json')
        r['reviewer'] = dict(id='SYNTHETIC_TEST_FIXTURE_NOT_REAL_REVIEW', kind='human', was_implementer=False, received_code_history_or_scores=False)
        r['playback'] = dict(kind='continuous_playback', speed=1, intervals=[[0, 1]], observation='Synthetic assertion for parser test only')
        r['sound'] = dict(kind='listening', intervals=[[0, 1]], listening_conditions='Synthetic fixture only', observation='Synthetic assertion only')
        r['observations'] = [dict(dimension=d, interval=[.4, .8], observation='Synthetic localized event', viewer_effect='Synthetic viewer effect')
                             for d in ['narrative_rhythm', 'motion_camera', 'focus_typography', 'sound_picture']]
        r['artistic_decision'] = 'approved'
        return r

    def check(self, r):
        return ad.check_review(self.packet, r)

    def test_consistent_declaration_is_not_verification(self):
        result = self.check(self.fixture())
        self.assertEqual(result['status'], 'evidence_record_consistent')
        self.assertNotIn('verified', result.keys())
        self.assertIn('does not prove', result['scope'])

    def test_screenshots_do_not_pass_motion_gate(self):
        for kind in ['screenshots', 'frame_sequence', 'optical_flow']:
            r = self.fixture(); r['playback']['kind'] = kind
            self.assertIn('full_normal_speed_motion_evidence_missing', self.check(r)['errors'])

    def test_metrics_do_not_pass_listening_gate(self):
        for kind in ['lufs', 'waveform', 'transcript', 'full_decode']:
            r = self.fixture(); r['sound']['kind'] = kind
            self.assertIn('full_actual_listening_evidence_missing', self.check(r)['errors'])

    def test_full_duration_required_for_both(self):
        for name in ['playback', 'sound']:
            r = self.fixture(); r[name]['intervals'] = [[0, .3]]
            self.assertEqual(self.check(r)['status'], 'evidence_incomplete')

    def test_real_gap_rejected(self):
        r = self.fixture(); r['playback']['intervals'] = [[0, .2], [.6, 1]]
        self.assertIn('full_normal_speed_motion_evidence_missing', self.check(r)['errors'])

    def test_slow_motion_diagnostic_is_not_normal_playback(self):
        r = self.fixture(); r['playback']['speed'] = .25
        self.assertIn('full_normal_speed_motion_evidence_missing', self.check(r)['errors'])

    def test_stale_movie_binding(self):
        r = self.fixture(); r['video_sha256'] = '0'*64
        self.assertIn('stale_or_missing_video', self.check(r)['errors'])

    def test_self_review_and_biased_context_rejected(self):
        for key in ['was_implementer', 'received_code_history_or_scores']:
            r = self.fixture(); r['reviewer'][key] = True
            self.assertIn('independent_review_missing_or_biased', self.check(r)['errors'])

    def test_localized_observations_valid_without_start_at_zero(self):
        self.assertEqual(self.check(self.fixture())['errors'], [])

    def test_missing_and_malformed_observation(self):
        for interval in [[], [1, 2], [True, 1], ['a', 'b'], None]:
            r = self.fixture(); r['observations'][0]['interval'] = interval
            self.assertIn('timecoded_observation_missing_narrative_rhythm', self.check(r)['errors'])

    def test_max_three_priority_fixes(self):
        r = self.fixture(); r['artistic_decision'] = 'needs_revision'
        r['priority_issues'] = [dict(id=str(i), interval=[.2, .5], impact='fixture', suggested_change='delete fixture') for i in range(4)]
        self.assertIn('too_many_priority_issues', self.check(r)['errors'])

    def test_approval_with_open_issues_rejected(self):
        r = self.fixture(); r['priority_issues'] = [dict(id='one', interval=[.2, .5], impact='fixture', suggested_change='delete fixture')]
        self.assertIn('approved_with_open_priority_issues', self.check(r)['errors'])

    def test_budget_stops_without_passing(self):
        r = self.fixture(); r['artistic_decision'] = 'needs_revision'; r['iteration']['round'] = 2
        result = self.check(r)
        self.assertTrue(result['iteration_budget_exhausted'])
        self.assertEqual(result['artistic_status'], 'needs_revision')
        self.assertEqual(result['next_action'], 'stop_and_report_remaining_tradeoffs')

    def test_too_many_changes(self):
        r = self.fixture(); r['iteration']['changes'] = ['a', 'b', 'c', 'd']
        self.assertIn('too_many_changes_this_round', self.check(r)['errors'])

    def test_tampered_packet_metadata_reprobed(self):
        pack = ad.read(self.packet); pack['media']['width'] = 999
        path = self.root/'packet/tampered.json'; ad.write(path, pack)
        self.assertIn('packet_media_mismatch', ad.check_review(path, self.fixture())['errors'])

    def test_missing_audio_actual_media_fails(self):
        silent = self.root/'silent.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(self.video), '-an', '-c:v', 'copy', str(silent)], check=True)
        out = self.root/'silent-packet'
        ad.packet(self.root/'brief.json', silent, out)
        self.assertEqual(ad.read(out/'technical-observations.json')['status'], 'failed')

    def test_clean_reviewer_brief_omits_implementation(self):
        brief = ad.read(self.root/'packet/brief.json')
        self.assertNotIn('skill_bindings', brief)
        self.assertNotIn('directions', brief)
        self.assertNotIn('iteration_budget', brief)

    def test_color_swap_is_not_a_distinct_direction(self):
        b = copy.deepcopy(self.brief)
        b['directions'][1] = copy.deepcopy(b['directions'][0]); b['directions'][1]['id'] = 'single-line'
        b['directions'][1]['color'] = 'different'
        self.assertIn('directions_only_cosmetically_different', ad.brief_errors(b))

    def test_real_seed_and_replay(self):
        a, b = ad.exploration(), ad.exploration()
        self.assertNotEqual(a['seed'], b['seed'])
        self.assertEqual(a['seed_source'], 'system_entropy_secrets')
        self.assertEqual(a['prompts'], ad.exploration(a['seed'])['prompts'])

    def test_no_overwrite_evidence(self):
        with self.assertRaises(FileExistsError):
            ad.write(self.packet, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
