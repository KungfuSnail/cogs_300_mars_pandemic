# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile

import time

# pylint: disable=no-member


# CONSTANTS
INFECTION_RATE = 0.16
IMMUNE_INFECTION_RATE = 0.05

DEATH_CHANCE = 0.25
CONTINUE_BEING_INFECTED_CHANCE = 0.50
HEAL_CHANCE = 0.25

#Unused:
# DEAD_INFECTION_RATE = ?


def create_hexagon(position, radius=50, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    if class_.cell_status == 0:
        cell_colour = (240, 240, 240)
    return class_(radius, position, colour=cell_colour)


def init_hexagons(num_x=30, num_y=30, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(-50, -50), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        for i in range(num_x):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons):
    """Renders hexagons on the screen"""
    screen.fill((0, 0, 0))
    for hexagon in hexagons:
        hexagon.render(screen)
        hexagon.render_highlight(screen, border_colour=(0, 0, 0)) 

        if hexagon.cell_status == 1: 
            hexagon.colour = (100, 100, 0)
        elif hexagon.cell_status == 2:
            hexagon.colour = (0, 0, 0)
        elif hexagon.cell_status == 3:
            hexagon.colour = (200, 200, 0)

    # # draw borders around colliding hexagons and neighbours
    # mouse_pos = pygame.mouse.get_pos()
    # colliding_hexagons = [
    #     hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
    # ]
    # for hexagon in colliding_hexagons:
    #     for neighbour in hexagon.compute_neighbours(hexagons):
    #         neighbour.render_highlight(screen, border_colour=(100, 100, 100))
    #     hexagon.render_highlight(screen, border_colour=(0, 0, 0))

    pygame.display.flip()

def next_turn_status_for_infected_cell(infected_hexagon):

    possible_statuses = [1, 2, 3]
    weights = [CONTINUE_BEING_INFECTED_CHANCE, DEATH_CHANCE, HEAL_CHANCE]
    status = random.choices(possible_statuses, weights=weights, k=1)[0]

    infected_hexagon.cell_status = status
    return infected_hexagon

def calculate_next_turn(hexagons):
    for target_hexagon in hexagons:

        num = 0
        print("##########")
        print("##########")
        print("##########")
        print("##########")
        print("GOing in")
        if target_hexagon.cell_status == 0:
            print("Cell not infected")
            print("##########")
            # Takes neighbour hexagon's health into account and calculates 
            # the chance the next turn the target cell will be infected
            chances_of_infection = 0
            for neighbour_hexagon in target_hexagon.compute_neighbours(hexagons):
                if neighbour_hexagon.cell_status == 1:
                    print("NEIGHBOUR WAS INFECTED!")
                    chances_of_infection = chances_of_infection + INFECTION_RATE
                elif neighbour_hexagon.cell_status == 3:
                    print("NEIGHBOUR WAS IMMUNE!")
                    chances_of_infection = chances_of_infection + IMMUNE_INFECTION_RATE
                elif neighbour_hexagon.cell_status == 0:
                    print("NEIGHBOUR WAS OK!")
                    chances_of_infection = chances_of_infection + 0
                else:
                    print("WHAT THE FUCK!")
                    print("Status is: ", target_hexagon.cell_status)
                
            print("Chances are ", chances_of_infection)
            # For example if the IMMUNE_INFECTION_RATE is 0.7, there is a 70% chance 
            # the boolean comes out TRUE and the cell gets infected
            
            print("##########")

            random_number = random.random()


            print("random number is ", random_number)
            if (chances_of_infection >= random_number):
                target_hexagon.cell_status = 1
                print("GOT INFECTED")
            else:
                print("DIDN'T GET INFECTED")
            
            chances_of_infection = 0 #resetting the chances
        elif target_hexagon.cell_status == 1:
            target_hexagon = next_turn_status_for_infected_cell(target_hexagon)
        elif target_hexagon.cell_status == 3:
            chances_of_infection = 0
            for neighbour_hexagon in target_hexagon.compute_neighbours(hexagons):
                if neighbour_hexagon.cell_status == 1:
                    print("NEIGHBOUR WAS INFECTED!")
                    chances_of_infection = chances_of_infection + INFECTION_RATE
                elif neighbour_hexagon.cell_status == 3:
                    print("NEIGHBOUR WAS IMMUNE!")
                    chances_of_infection = chances_of_infection + IMMUNE_INFECTION_RATE
                elif neighbour_hexagon.cell_status == 0:
                    print("NEIGHBOUR WAS OK!")
                    chances_of_infection = chances_of_infection + 0
                else:
                    print("WHAT THE FUCK!")
                    print("Status is: ", target_hexagon.cell_status)
                
            print("Chances are ", chances_of_infection)
            # For example if the IMMUNE_INFECTION_RATE is 0.7, there is a 70% chance 
            # the boolean comes out TRUE and the cell gets infected
            
            print("##########")

            random_number = random.random()


            print("random number is ", random_number)
            if (chances_of_infection >= random_number):
                target_hexagon.cell_status = 1
                print("GOT INFECTED")
            else:
                print("DIDN'T GET INFECTED")
            
            chances_of_infection = 0 #resetting the chances
            
    
    
    print("##########")
    print("#")
    print("#")
    print("#")



            

        

def make_neighbours_yellow_lol(hexagons, hexagon):
    for neighbour_hexagon in hexagon.compute_neighbours(hexagons):
        neighbour_hexagon.colour = (100, 100, 0)
    

def main():
    """Main function"""
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=True)
    terminated = False

    for i in range(5):
        random.choice(hexagons).cell_status = 1

        # time.sleep(2)
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    calculate_next_turn(hexagons)  

        for hexagon in hexagons:
            hexagon.update()



        
        render(screen, hexagons)
        clock.tick(60)

    pygame.display.quit()


if __name__ == "__main__":
    main()
