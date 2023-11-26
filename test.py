import pytest
import random

from agents import (Wall, Gold, Explorer, Thing, Bump, Glitter,
                    WumpusEnvironment, Pit)

def test_WumpusEnvironment():
    def constant_prog(percept):
        return percept

    # initialize Wumpus Environment
    w = WumpusEnvironment(constant_prog)

    # check if things are added properly
    assert len([x for x in w.things if isinstance(x, Wall)]) == 20
    assert any(map(lambda x: isinstance(x, Gold), w.things))
    assert any(map(lambda x: isinstance(x, Explorer), w.things))
    assert not any(map(lambda x: not isinstance(x, Thing), w.things))

    # check that gold and wumpus are not present on (1,1)
    assert not any(map(lambda x: isinstance(x, Gold) or isinstance(x, WumpusEnvironment), w.list_things_at((1, 1))))

    # check if w.get_world() segments objects correctly
    assert len(w.get_world()) == 6
    for row in w.get_world():
        assert len(row) == 6

    # start the game!
    agent = [x for x in w.things if isinstance(x, Explorer)][0]
    gold = [x for x in w.things if isinstance(x, Gold)][0]
    pit = [x for x in w.things if isinstance(x, Pit)][0]

    assert not w.is_done()

    # check Walls
    agent.location = (1, 2)
    percepts = w.percept(agent)
    assert len(percepts) == 5
    assert any(map(lambda x: isinstance(x, Bump), percepts[0]))

    # check Gold
    agent.location = gold.location
    percepts = w.percept(agent)
    assert any(map(lambda x: isinstance(x, Glitter), percepts[4]))
    agent.location = (gold.location[0], gold.location[1] + 1)
    percepts = w.percept(agent)
    assert not any(map(lambda x: isinstance(x, Glitter), percepts[4]))

    # check agent death
    agent.location = pit.location
    assert w.in_danger(agent)
    assert not agent.alive
    assert agent.killed_by == Pit.__name__
    assert agent.performance == -1000

    assert w.is_done()


def test_WumpusEnvironmentActions():
    random.seed(9)
    def constant_prog(percept):
        return percept

    # initialize Wumpus Environment
    w = WumpusEnvironment(constant_prog)

    agent = [x for x in w.things if isinstance(x, Explorer)][0]
    gold = [x for x in w.things if isinstance(x, Gold)][0]
    pit = [x for x in w.things if isinstance(x, Pit)][0]

    agent.location = (1, 1)
    assert agent.direction.direction == "right"
    w.execute_action(agent, 'TurnRight')
    assert agent.direction.direction == "down"
    w.execute_action(agent, 'TurnLeft')
    assert agent.direction.direction == "right"
    w.execute_action(agent, 'Forward')
    assert agent.location == (2, 1)

    agent.location = gold.location
    w.execute_action(agent, 'Grab')
    assert agent.holding == [gold]

    agent.location = (1, 1)
    w.execute_action(agent, 'Climb')
    assert not any(map(lambda x: isinstance(x, Explorer), w.things))

    assert w.is_done()

if __name__ == "__main__":
    pytest.main()