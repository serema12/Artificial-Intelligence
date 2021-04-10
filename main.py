from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
from agent import CSPAgent,ImprovedSCPAgent


class MineSweeper():
    CSPAgent = "csp_agent"
    ImprovedSCPAgent = "improved_csp_agent"

    def __init__(self,
                 ground_dimension = None,
                 mine_density = None,
                 agent_name = None,
                 end_game_on_mine_hit = True):
        self.ground_dimension = ground_dimension
        self.mine_density = mine_density
        self.agent_name = agent_name
        self.end_game_on_mine_hit = end_game_on_mine_hit

    def create_environment(self):

        # Create the maze
        self.env = Environment(n = self.ground_dimension,
                               mine_density = self.mine_density,
                               end_game_on_mine_hit = self.end_game_on_mine_hit)
        self.env.generate_environment()

    def run(self):

        # Use the agent to find mines in our mine-sweeper environment
        if self.agent_name == self.CSPAgent:
            self.mine_sweeper_agent = CSPAgent(env = self.env,
                                               end_game_on_mine_hit = self.end_game_on_mine_hit)
        elif self.agent_name == self.ImprovedSCPAgent:
            self.mine_sweeper_agent = ImprovedSCPAgent(env = self.env,
                                               end_game_on_mine_hit = self.end_game_on_mine_hit)

        self.mine_sweeper_agent.play()
        metrics = self.mine_sweeper_agent.get_gameplay_metrics()
        # print("Game won = ", str(metrics["game_won"]))
        print("Number of mines hit = ", str(metrics["number_of_mines_hit"]))
        print("Number of mines flagged correctly = ", str(metrics["number_of_mines_flagged_correctly"]))
        print("Number of cells flagged incorrectly = ", str(metrics["number_of_cells_flagged_incorrectly"]))

        self.env.render_env(100)

    def get_performance(self):
        performance_dict_1 = dict()
        performance_dict_2 = dict()
        for mine_density in np.arange(0.01, 0.5,0.01):
            print(mine_density)
            performance_dict_1[mine_density] = dict()
            performance_dict_2[mine_density] = dict()

            final_scores_1 = list()
            mines_hit_1 = list()
            correct_mines_1 = list()
            incorrect_mines_1 = list()

            final_scores_2 = list()
            mines_hit_2 = list()
            correct_mines_2 = list()
            incorrect_mines_2 = list()
            for _ in range(10):
                env = Environment(n = 10, mine_density = mine_density, end_game_on_mine_hit = False)
                env.generate_environment()

                agent1 = CSPAgent(env = env, end_game_on_mine_hit = False)
                agent1.play()

                agent2 = ImprovedSCPAgent(env = env, end_game_on_mine_hit = False)
                agent2.play()


                metrics_1 = agent1.get_gameplay_metrics()
                final_scores_1.append(metrics_1["final_score"])
                mines_hit_1.append(metrics_1["number_of_mines_hit"])

                metrics_2 = agent2.get_gameplay_metrics()
                final_scores_2.append(metrics_2["final_score"])
                mines_hit_2.append(metrics_2["number_of_mines_hit"])

            final_score_1 = np.mean(final_scores_1)
            num_mines_hit_1 = np.mean(mines_hit_1)

            final_score_2 = np.mean(final_scores_2)
            num_mines_hit_2 = np.mean(mines_hit_2)

            performance_dict_1[mine_density]["final_score"] = final_score_1
            performance_dict_1[mine_density]["number_of_mines_hit"] = num_mines_hit_1

            performance_dict_2[mine_density]["final_score"] = final_score_2
            performance_dict_2[mine_density]["number_of_mines_hit"] = num_mines_hit_2

        mine_densities_1 = performance_dict_1.keys()
        final_scores_1 = [performance_dict_1[density]["final_score"] for density in performance_dict_1]
        mines_hit_1 = [performance_dict_1[density]["number_of_mines_hit"] for density in performance_dict_1]

        mine_densities_2 = performance_dict_2.keys()
        final_scores_2 = [performance_dict_2[density]["final_score"] for density in performance_dict_2]
        mines_hit_2 = [performance_dict_2[density]["number_of_mines_hit"] for density in performance_dict_2]

        plt.plot(mine_densities_1, final_scores_1, marker = 'o', label = "Normal CSP Agent")
        plt.plot(mine_densities_2, final_scores_2, marker = 'o', label = "Improved CSP Agent")
        plt.xlabel("Mine Density")
        plt.ylabel("Average Final Score")
        plt.savefig('avg_final_score_bonus.png')
        plt.legend()
        plt.close()
        
        plt.plot(mine_densities_1, mines_hit_1, marker = 'o', label = "Normal CSP Agent")
        plt.plot(mine_densities_2, mines_hit_2, marker = 'o', label = "Improved CSP Agent")
        plt.xlabel("Mine Density")
        plt.ylabel("Average Density of Mines Hit")
        plt.savefig('avg_density_of_mines_hit_bonus.png')
        
        plt.legend()
        plt.close()
        return performance_dict_1, performance_dict_2

        return performance_dict


if __name__ == "__main__":
    #CSP agent: csp_agent, Improve agent: improved_csp_agent
    mine_sweeper = MineSweeper(ground_dimension = 10,
                               mine_density = 0.3,
                               agent_name = "csp_agent", 
                               end_game_on_mine_hit = False)

    #mine_sweeper.create_environment()
    #mine_sweeper.run()
    mine_sweeper.get_performance()