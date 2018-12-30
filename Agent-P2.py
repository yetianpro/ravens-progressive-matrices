# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image, ImageChops, ImageOps, ImageStat, ImageFilter
import numpy as np

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    def read_input_image_3x3(self, figures):
        try:
            imageA = Image.open(figures['A'].visualFilename).convert('L')
            imageB = Image.open(figures['B'].visualFilename).convert('L')
            imageC = Image.open(figures['C'].visualFilename).convert('L')
            imageD = Image.open(figures['D'].visualFilename).convert('L')
            imageE = Image.open(figures['E'].visualFilename).convert('L')
            imageF = Image.open(figures['F'].visualFilename).convert('L')
            imageG = Image.open(figures['G'].visualFilename).convert('L')
            imageH = Image.open(figures['H'].visualFilename).convert('L')
        except IOError:
            print("at least 1 input image not found")
        return (imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH)

    def read_answer_image_3x3(self, figures):
        try:
            a1 = Image.open(figures['1'].visualFilename).convert('L')
            a2 = Image.open(figures['2'].visualFilename).convert('L')
            a3 = Image.open(figures['3'].visualFilename).convert('L')
            a4 = Image.open(figures['4'].visualFilename).convert('L')
            a5 = Image.open(figures['5'].visualFilename).convert('L')
            a6 = Image.open(figures['6'].visualFilename).convert('L')
            a7 = Image.open(figures['7'].visualFilename).convert('L')
            a8 = Image.open(figures['8'].visualFilename).convert('L')
        except IOError:
            print("at least 1 input image not found")
        return (a1,a2,a3,a4,a5,a6,a7,a8)

    #"shape", "size", "fill", "angle", "inside", "alignment", "overlaps", "above", "left-of", "width", "height"

    # Shape: Square, pac-man, circle, pentagon, triangle, star, heart, plus, right-angle, octagon, diamond
    # Fill: yes, no, right-half, left-half
    # size: very large, huge
    # angle: <integer>
    # inside: <object/shape indicated by letter>
    # alignment: bottom-right, top-right, bottom-let, top-left
    # above: <object/shape indicated by letter>

    def fill_rate(self, image):
        pixels = np.array(image)
        count, white = 0,0

        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                count += 1
                if pixels[i][j] == 0:
                    white +=1 
        rate = float(count - white) / count
        return round((1-rate) * 100, 3)

    def find_component(self,image):
        component,connected = 0,0
        row, col = image.size
        counted_set = []

        array1 = np.array(image)
        for i in range(1,len(array1)-1):
            for j in range(1,len(array1[0])-1):
                add_flg = False
                if array1[i][j]  < 235 :
                    neighbors = [(i-1,j-1),(i-1,j),(i,j-1),(i+1,j+1),(i+1,j),(i,j+1),(i+1,j-1),(i-1,j+1)]
                    for pixel in neighbors:
                        for set_index in range(len(counted_set)):
                            if pixel in counted_set[set_index]:
                                counted_set[set_index].append((i,j))
                                add_flg = True
                                break

                    if not add_flg:
                        component += 1
                        counted_set.append([(i,j)])

        # if component > 1:
        #     for i in range(len(counted_set)-1):
        #         for j in range(i+1, len(counted_set)):
        #             connect_flg = False
        #             for point in counted_set[i]:
        #                 x = point[0]
        #                 y = point[1]
        #                 neighbors = [(x-1,y-1),(x-1,y),(x,y-1),(x+1,y+1),(x+1,y),(x,y+1),(x+1,y-1),(x-1,y+1)]
        #                 for neighbor in neighbors:
        #                     if neighbor in counted_set[j]:
        #                         connect_flg = True
        #                         break
        #                 if connect_flg:
        #                     break
        #             if connect_flg:
        #                 connected += 1
        #     component -= connected
        return component

    def DPR(self, image1, image2):
        ratio = np.abs(self.single_fill_rate(image1), self.single_fill_rate(image2))
        return ratio

    def IPR(self, image1, image2):
        array1 = np.array(image1)
        array2 = np.array(image2)
        count, same = 0,0

        for i in range(len(array1)):
            for j in range(len(array1[0])):
                count += 1
                if array1[i][j] == array2[i][j]:
                    same +=1 
        rate = round(float(same) / count * 100,3)
        return rate

    def difference(self, image1, image2):
        array1 = np.array(image1)
        array2 = np.array(image2)
        diff = np.sum(np.sqrt(array1.astype('float') - array2.astype('float')))
        diff = diff / (len(array1) * len(array1[0]))
        return diff

    def find_same(self, image1, image2):
        count = 0
        diff = np.array(ImageChops.difference(image1,image2))
        for i in range(len(diff)):
            for j in range(len(diff[0])):
                if diff[i][j] != 0:
                    count +=1 
        if count <= 1005:
            return True
        return False

    def find_flip(self, image1, image2):
        count1, count2, count3 = 0,0,0

        diff1 = np.array(ImageChops.difference(image1,image2))
        diff2 = np.array(ImageChops.difference(image1.transpose(Image.FLIP_LEFT_RIGHT),image2))
        diff3 = np.array(ImageChops.difference(image1.transpose(Image.FLIP_TOP_BOTTOM),image2))
        
        for i in range(len(diff1)):
            for j in range(len(diff1[0])):
                if diff1[i][j] != 0:
                    count1 +=1 
                if diff2[i][j] != 0:
                    count2 += 1
                if diff3[i][j] != 0:
                    count3 += 1  

        min_diff = min(count2, count3)
        #print(count2,count3)
        if min_diff >= 790:
            return (False, "not flip")
        else:
            if count2 <= count3:
                return (True, "flip_left_right")
            else:
                return (True, "flip_top_bottom")

    def find_rotation(self, image1, image2):
        count1, count2, count3, count4 = 0,0,0,0

        diff1 = np.array(ImageChops.difference(image1,image2))
        diff2 = np.array(ImageChops.difference(image1.rotate(90),image2))
        diff3 = np.array(ImageChops.difference(image1.rotate(180),image2))
        diff4 = np.array(ImageChops.difference(image1.rotate(270),image2))
    
        for i in range(len(diff1)):
            for j in range(len(diff1[0])):
                if diff1[i][j] != 0:
                    count1 +=1 
                if diff2[i][j] != 0:
                    count2 += 1
                if diff3[i][j] != 0:
                    count3 += 1
                if diff4[i][j] != 0:
                    count4 += 1
        min_diff = min(count2, count3, count4)
        print(count2,count3,count4)
        if min_diff >= 825:
            return (False, 0)
        else:
            if count2 == min_diff:
                return (True, 90)
            elif count3 == min_diff:
                return (True, 180)
            else:
                return (True, 270)

    def fill_rate_analysis(self, input_fill_rates, answer_fill_rates, threshold):
        # each row same, except center
        # row increase & col increase & opp same, row increase & col increase & opp same not E,
        #print(problem_name, input_fill_rates, answer_fill_rates)
        fill_same = {"AB": np.abs(input_fill_rates[0] - input_fill_rates[1]) < threshold,
                     "AC": np.abs(input_fill_rates[0] - input_fill_rates[2]) < threshold,
                     "BC": np.abs(input_fill_rates[1] - input_fill_rates[2]) < threshold,
                     "DE": np.abs(input_fill_rates[3] - input_fill_rates[4]) < threshold,
                     "DF": np.abs(input_fill_rates[3] - input_fill_rates[5]) < threshold,
                     "EF": np.abs(input_fill_rates[4] - input_fill_rates[5]) < threshold,
                     "GH": np.abs(input_fill_rates[6] - input_fill_rates[7]) < threshold,
                     "AG": np.abs(input_fill_rates[0] - input_fill_rates[6]) < threshold,
                     "BH": np.abs(input_fill_rates[1] - input_fill_rates[7]) < threshold,

                     "AD": np.abs(input_fill_rates[0] - input_fill_rates[3]) < threshold,
                     "DG": np.abs(input_fill_rates[3] - input_fill_rates[6]) < threshold,
                     "AG": np.abs(input_fill_rates[0] - input_fill_rates[6]) < threshold,
                     "BE": np.abs(input_fill_rates[1] - input_fill_rates[4]) < threshold,
                     "EH": np.abs(input_fill_rates[4] - input_fill_rates[7]) < threshold,
                     "BH": np.abs(input_fill_rates[1] - input_fill_rates[7]) < threshold,
                     "CF": np.abs(input_fill_rates[2] - input_fill_rates[5]) < threshold,

                     "BD": np.abs(input_fill_rates[1] - input_fill_rates[3]) < threshold,
                     "CE": np.abs(input_fill_rates[2] - input_fill_rates[4]) < threshold,
                     "EG": np.abs(input_fill_rates[4] - input_fill_rates[6]) < threshold,
                     "CG": np.abs(input_fill_rates[2] - input_fill_rates[6]) < threshold,
                     "FH": np.abs(input_fill_rates[5] - input_fill_rates[7]) < threshold
                     }
        fill_increase = {"AD": input_fill_rates[3] - input_fill_rates[0] > threshold,
                         "AE": input_fill_rates[4] - input_fill_rates[0] > threshold,
                         "AB": input_fill_rates[1] - input_fill_rates[0] > threshold,
                         "DG": input_fill_rates[6] - input_fill_rates[3] > threshold,
                         "BC": input_fill_rates[2] - input_fill_rates[1] > threshold,
                         "CF": input_fill_rates[5] - input_fill_rates[2] > threshold,
                         "GH": input_fill_rates[7] - input_fill_rates[6] > threshold,
                         }
        fill_decrease = {"CF": input_fill_rates[2] - input_fill_rates[5] > threshold,
                         "GH": input_fill_rates[6] - input_fill_rates[7] > threshold,
                         }
        #print(fill_same)
        #print(fill_increase)
        possible_answers = []
        if fill_same["AB"] and fill_same["BC"] and fill_same["AC"] and fill_same["DE"] and fill_same["EF"] and fill_same["DF"] and fill_same["GH"]:
            possible_fill_rate = (input_fill_rates[6] - threshold, input_fill_rates[6] + threshold)
            for index, value in enumerate(answer_fill_rates):
                if value > possible_fill_rate[0] and value < possible_fill_rate[1]:
                    possible_answers.append(index + 1)
            #print("each row same")
            return possible_answers
        elif fill_same["AD"] and fill_same["DG"] and fill_same["AG"] and fill_same["BE"] and fill_same["EH"] and fill_same["BH"] and fill_same["CF"]:
            possible_fill_rate = (input_fill_rates[5] - threshold, input_fill_rates[5] + threshold)
            for index, value in enumerate(answer_fill_rates):
                if value > possible_fill_rate[0] and value < possible_fill_rate[1]:
                    possible_answers.append(index + 1)
            #print("each col same")
            return possible_answers
        elif fill_same["AC"] and fill_same["DF"] and fill_same["AG"] and fill_same["BH"]:
            possible_fill_rate = (input_fill_rates[6] - threshold, input_fill_rates[6] + threshold)
            for index, value in enumerate(answer_fill_rates):
                if value > possible_fill_rate[0] and value < possible_fill_rate[1]:
                    possible_answers.append(index + 1)
            #print("center")
            return possible_answers
        elif fill_same["BD"] and fill_same["CG"] and fill_increase["GH"] and fill_increase["CF"]:
            possible_fill_rate = input_fill_rates[7]
            #print(possible_fill_rate)
            for index, value in enumerate(answer_fill_rates):
                if value >= possible_fill_rate+threshold:
                    possible_answers.append(index + 1)
            #print("opp increase")
            return possible_answers
        elif fill_same["BD"] and fill_same["CG"] and fill_decrease["GH"] and fill_decrease["CF"]:
            possible_fill_rate = input_fill_rates[7]
            #print(possible_fill_rate)
            for index, value in enumerate(answer_fill_rates):
                if value <= possible_fill_rate-threshold:
                    possible_answers.append(index + 1)
            #print("opp decrease")
            return possible_answers

        return [1,2,3,4,5,6,7,8]

    def center_analysis(self, imageA,imageC,imageG, after_fill_rates, answers):

        input_flip = {"AC" : self.find_flip(imageA, imageC),
                "AG" : self.find_flip(imageA, imageG)}
        # input_rotation = {
        #         "AC" : self.find_rotation(imageA, imageC),
        #         "AG" : self.find_rotation(imageA, imageG)}


        possible_answers = []
        if input_flip["AC"][0] and input_flip["AG"][0]:
            for index in after_fill_rates:
                if self.find_same(answers[index-1], imageG.transpose(Image.FLIP_LEFT_RIGHT)) or self.find_same(answers[index-1], imageC.transpose(Image.FLIP_TOP_BOTTOM)):
                    possible_answers.append(index)
            if len(possible_answers):
                return possible_answers

        return answers

    def guess(self,imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            answers):
        possible_answers = [1,2,3,4,5,6,7,8]
        for index,value in enumerate(answers):
            if self.find_same(imageA, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageB, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageC, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageD, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageE, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageF, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageG, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.find_same(imageH, value):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
        return possible_answers

    def component_analysis(self, imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            answers):

        input_components = [self.find_component(imageA),self.find_component(imageB),self.find_component(imageC),
                      self.find_component(imageD),self.find_component(imageE),self.find_component(imageF),
                      self.find_component(imageG),self.find_component(imageH)]

        # answer_components = [self.find_component(answer1),self.find_component(answer2),self.find_component(answer3),
        #               self.find_component(answer4),self.find_component(answer5),self.find_component(answer6),
        #               self.find_component(answer7),self.find_component(answer8)]

        answer_components = [self.find_component(answer) for answer in answers]

        # all the same, each row same, each column same, flip same
        avg_component = np.average(np.array(input_components))
        input_components = np.array(input_components)

        possible_answers = []
        #print(problem_name.split(" ")[2],"component analysis",input_components,answer_components)

        if avg_component >= 5:
            #print("no component analysis")
            return answers
        else:
            same_all = np.array(input_components == input_components[0])
            same_row1 = np.array(input_components == input_components[0])[0:3]
            same_row2 = np.array(input_components == input_components[3])[3:6]
            same_row3 = np.array(input_components == input_components[6])[6:]
            same_col1 = [np.array(input_components == input_components[0])[0],np.array(input_components == input_components[0])[3],np.array(input_components == input_components[0])[6]]
            same_col2 = [np.array(input_components == input_components[1])[1],np.array(input_components == input_components[1])[4],np.array(input_components == input_components[1])[7]]
            same_col3 = [np.array(input_components == input_components[2])[2],np.array(input_components == input_components[2])[5]]
            same_opp = np.sum(np.array([input_components[1] == input_components[3],input_components[2] == input_components[6],input_components[5] == input_components[7]]))
            if np.sum(same_all) == 8:
                for index,value in enumerate(answer_components):
                    if value == input_components[0]:
                        possible_answers.append(index+1)
                #print("all_same")
                return possible_answers
            elif np.sum(same_row1) == 3 and np.sum(same_row2) == 3 and np.sum(same_row3) == 2:
                for index,value in enumerate(answer_components):
                    if value == input_components[6]:
                        possible_answers.append(index+1)
                #print("row_same")
                return possible_answers
            elif np.sum(same_col1) == 3 and np.sum(same_col2) == 3 and np.sum(same_col3) == 2:
                for index,value in enumerate(answer_components):
                    if value == input_components[2]:
                        possible_answers.append(index+1)
                #print("col_same")
                return possible_answers
            elif same_opp == 3:
                # if input_components[2] > input_components[1] and input_components[5] > input_components[2]:
                if input_components[5] > input_components[2]:
                    for index,value in enumerate(answer_components):
                        if value > input_components[5]:
                            possible_answers.append(index+1)
                    #print("increase")
                    return possible_answers
                elif input_components[5] == input_components[2]:
                    for index,value in enumerate(answer_components):
                        if value == input_components[5]:
                            possible_answers.append(index+1)
                    #print("same increase")
                    return possible_answers
                elif input_components[5] < input_components[2]:
                    for index, value in enumerate(answer_components):
                        if value < input_components[5]:
                            possible_answers.append(index + 1)
                    #print("decrease")
                    return possible_answers
            else:
                if (input_components[1]-input_components[0]) == (input_components[2]-input_components[1]) and (input_components[4]-input_components[3]) == (input_components[5]-input_components[4]):
                    diff = input_components[7] - input_components[6] + input_components[7]
                    for index, value in enumerate(answer_components):
                        if value == diff:
                            possible_answers.append(index + 1)
                    return possible_answers
                if (input_components[3]-input_components[0]) == (input_components[6]-input_components[3]) and (input_components[4]-input_components[1]) == (input_components[6]-input_components[4]):
                    diff = input_components[5] - input_components[2] + input_components[5]
                    for index, value in enumerate(answer_components):
                        if value == diff:
                            possible_answers.append(index + 1)
                    return possible_answers

        return answers

    def Solve(self,problem):
        global problem_name
        problem_type = problem.problemType
        problem_name = problem.name
        problem_diffcult = problem.name.split()[0]
        figures = problem.figures

        if problem_type == "3x3":
            imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH = self.read_input_image_3x3(figures)
            answer1,answer2,answer3,answer4,answer5,answer6,answer7,answer8 = self.read_answer_image_3x3(figures)
            answers = (answer1,answer2,answer3,answer4,answer5,answer6,answer7,answer8)

            # if problem_name.split(" ")[0] == 'Challenge':
            #     return np.random.choice([1,2,3,4,5,6,7,8])
            # if problem_name in ['Basic Problem C-08','Basic Problem C-09','Basic Problem C-12','Basic Problem C-02']:
            #     return -1


            input_fill_rates = [self.fill_rate(imageA),self.fill_rate(imageB),self.fill_rate(imageC),self.fill_rate(imageD),
                          self.fill_rate(imageE),self.fill_rate(imageF),self.fill_rate(imageG),self.fill_rate(imageH)]
            answer_fill_rates = [self.fill_rate(answer1),self.fill_rate(answer2),self.fill_rate(answer3),
                                 self.fill_rate(answer4),self.fill_rate(answer5),self.fill_rate(answer6),
                                 self.fill_rate(answer7),self.fill_rate(answer8)]
            threshold = 0.35
            after_fill_rates = self.fill_rate_analysis(input_fill_rates, answer_fill_rates, threshold)
            print(problem_name.split(" ")[2],"fill analysis", after_fill_rates)

            if len(after_fill_rates) == 0:
                # fill rate failed
                return np.random.choice([1,2,3,4,5,6,7,8])
            elif len(after_fill_rates) == 1:
                return after_fill_rates[0]
            elif len(after_fill_rates) == 8:
                guess_answer = self.guess(imageA, imageB, imageC, imageD, imageE, imageF, imageG, imageH, answers)
                print(problem_name.split(" ")[2], "guess", guess_answer)
                return np.random.choice(guess_answer)
            else:
                selected_answer = []
                for index in after_fill_rates:
                    selected_answer.append(answers[index - 1])

                after_center = self.center_analysis(imageA, imageC, imageG, after_fill_rates, answers)
                if len(after_center) == 1:
                    print(problem_name.split(" ")[2], "center analysis", after_center)
                    return after_center[0]

                selected_component = self.component_analysis(imageA, imageB, imageC, imageD, imageE, imageF, imageG,
                                                          imageH, selected_answer)
                after_component = []
                if len(selected_component) == len(after_fill_rates) or len(selected_component) == 0:
                    guess_answer = self.guess(imageA, imageB, imageC, imageD, imageE, imageF, imageG, imageH, selected_answer)
                    print(problem_name.split(" ")[2],"guess", guess_answer)
                    return np.random.choice(guess_answer)
                    #return np.random.choice(after_fill_rates)

                for index in selected_component:
                    after_component.append(after_fill_rates[index-1])

                if len(after_component) == 1:
                    print(problem_name.split(" ")[2],"component analysis", after_component)
                    return after_component[0]
                else:
                    return np.random.choice(after_component)
                    # common = list(set(after_fill_rates) & set(after_component))
                    # if len(common) == 1:
                    #     return common[0]
                    # elif len(common) == 0:
                    #     return np.random.choice(after_fill_rates)
                    # else:
                    #     return np.random.choice(common)
        else:
            return -1


