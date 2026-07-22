#!/usr/bin/env python3
"""A minimal Gym-style RL environment wrapping an Isaac Sim cartpole, with a
random policy by default and an optional PPO training loop (stable-baselines3).

This shows the env contract (reset/step/reward/done) that Isaac Lab / Gym use.
"""
import argparse
import numpy as np
from isaacsim import SimulationApp

ap = argparse.ArgumentParser()
ap.add_argument('--headless', action='store_true')
ap.add_argument('--train', action='store_true',
                help='run a short PPO training (needs stable-baselines3+gym)')
args, _ = ap.parse_known_args()
sim_app = SimulationApp({"headless": args.headless or args.train})

from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.articulations import Articulation
from omni.isaac.nucleus import get_assets_root_path


class CartpoleEnv:
    """Bare-bones environment: balance the pole by pushing the cart."""
    def __init__(self, headless):
        self.world = World(stage_units_in_meters=1.0)
        self.world.scene.add_default_ground_plane()
        usd = get_assets_root_path() + "/Isaac/Robots/Cartpole/cartpole.usd"
        add_reference_to_stage(usd, "/World/Cartpole")
        self.robot = self.world.scene.add(
            Articulation("/World/Cartpole", name="cartpole"))
        self.world.reset()
        self.cart_dof = 0
        self.pole_dof = 1
        self.max_steps = 500

    def reset(self):
        self.world.reset()
        self.robot.set_joint_positions(
            np.array([0.0, np.random.uniform(-0.05, 0.05)]))
        self.steps = 0
        return self._obs()

    def _obs(self):
        q = self.robot.get_joint_positions()
        dq = self.robot.get_joint_velocities()
        return np.array([q[self.cart_dof], dq[self.cart_dof],
                         q[self.pole_dof], dq[self.pole_dof]], np.float32)

    def step(self, action):
        force = float(np.clip(action, -1, 1)) * 30.0
        self.robot.set_joint_efforts(np.array([force, 0.0]))
        self.world.step(render=False)
        self.steps += 1
        obs = self._obs()
        pole_angle = obs[2]
        done = abs(pole_angle) > 0.4 or self.steps >= self.max_steps
        reward = 1.0 - abs(pole_angle)
        return obs, reward, done, {}


def random_policy(env, episodes=5):
    for ep in range(episodes):
        env.reset(); total = 0.0; done = False
        while not done:
            _, r, done, _ = env.step(np.random.uniform(-1, 1))
            total += r
        print(f"episode {ep}: return={total:.1f}")


def main():
    env = CartpoleEnv(headless=args.headless or args.train)
    if args.train:
        try:
            import gymnasium as gym
            from gymnasium import spaces
            from stable_baselines3 import PPO

            class GymWrap(gym.Env):
                def __init__(self, e):
                    self.e = e
                    self.action_space = spaces.Box(-1, 1, (1,), np.float32)
                    self.observation_space = spaces.Box(
                        -np.inf, np.inf, (4,), np.float32)
                def reset(self, *a, **k):
                    return self.e.reset(), {}
                def step(self, action):
                    o, r, d, i = self.e.step(action[0])
                    return o, r, d, False, i

            model = PPO("MlpPolicy", GymWrap(env), verbose=1)
            model.learn(total_timesteps=5000)
            model.save("cartpole_ppo")
            print("Saved cartpole_ppo.zip")
        except Exception as e:
            print("Training path unavailable:", e)
            random_policy(env)
    else:
        random_policy(env)
    sim_app.close()


if __name__ == '__main__':
    main()
