from typing import TYPE_CHECKING
import gymnasium as gym

if TYPE_CHECKING:
    from osupy.env import OsuPyEnv


class MoverObservation(gym.ObservationWrapper):
    def __init__(self, env):
        self.env: "OsuPyEnv" = env  # type: ignore
        super().__init__(env)
        self.observation_space = gym.spaces.Dict(
            {
                "mouse_x": gym.spaces.Box(low=0, high=1, shape=(1,)),
                "mouse_y": gym.spaces.Box(low=0, high=1, shape=(1,)),
                "next_note_x": gym.spaces.Box(low=0, high=1, shape=(1,)),
                "next_note_y": gym.spaces.Box(low=0, high=1, shape=(1,)),
            }
        )

    def observation(self, observation):
        try:
            return {
                "mouse_x": (self.env.osu.mouse.x / self.env.osu.width),
                "mouse_y": (self.env.osu.mouse.y / self.env.osu.height),
                "next_note_x": (
                    self.env.osu.renderer.point_to_render[0] / self.env.osu.width
                ),
                "next_note_y": (
                    self.env.osu.renderer.point_to_render[1] / self.env.osu.height
                ),
            }
        except IndexError:
            return {
                "mouse_x": (self.env.osu.mouse.x / self.env.osu.width),
                "mouse_y": (self.env.osu.mouse.y / self.env.osu.height),
                "next_note_x": (0),
                "next_note_y": (0),
            }
