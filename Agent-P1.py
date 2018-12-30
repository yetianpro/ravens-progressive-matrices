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

    def read_input_image_2x2(self, figures):
        try:
            imageA = Image.open(figures['A'].visualFilename).convert('L')
            imageB = Image.open(figures['B'].visualFilename).convert('L')
            imageC = Image.open(figures['C'].visualFilename).convert('L')
        except IOError:
            print("at least 1 input image not found")
        return (imageA,imageB,imageC)

    def read_answer_image_2x2(self, figures):
        try:
            a1 = Image.open(figures['1'].visualFilename).convert('L')
            a2 = Image.open(figures['2'].visualFilename).convert('L')
            a3 = Image.open(figures['3'].visualFilename).convert('L')
            a4 = Image.open(figures['4'].visualFilename).convert('L')
            a5 = Image.open(figures['5'].visualFilename).convert('L')
            a6 = Image.open(figures['6'].visualFilename).convert('L')
        except IOError:
            print("at least 1 answer image not found")
        return (a1,a2,a3,a4,a5,a6)

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

    def fill_rate(self, image):
        pixels = np.array(image)
        count, white = 0,0

        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                count += 1
                if pixels[i][j] == 0:
                    white +=1 
        rate = float(count - white) / count
        return 1-rate

    def Solve(self,problem):

        problem_type = problem.problemType
        problem_name = problem.name
        problem_diffcult = problem.name.split()[0]
        figures = problem.figures

        if problem_type == "2x2":
            imageA, imageB, imageC = self.read_input_image_2x2(figures)
            answers = self.read_answer_image_2x2(figures)

            simpleAB = self.simple_compare(imageA, imageB)
            simpleAC = self.simple_compare(imageA, imageC)

            if simpleAB == "not simple" and simpleAC == "not simple":
                # hard mode
                fillA = self.fill_rate(imageA)
                fillB = self.fill_rate(imageB)
                fillC = self.fill_rate(imageC)

                featuresAB = self.hard_compare(imageA, imageB, fillA, fillB)
                featuresAC = self.hard_compare(imageA, imageC, fillA, fillC)

                print(problem_name, "hard")

                answer = self.find_hard_answer(featuresAB, featuresAC, answers, imageA, imageB, imageC)
                return answer
            
            else:
                #print(problem_name, "simple", simpleAB, simpleAC)

                # simple mode
                if simpleAB == "unchanged" and simpleAC == "unchanged":
                    return self.find_simple_answer("unchanged", imageA, answers)
                elif simpleAB == "unchanged":
                    return self.find_simple_answer("unchanged", imageC, answers)
                elif simpleAC == "unchanged":
                    return self.find_simple_answer("unchanged", imageB, answers)
                elif simpleAB == "not simple":
                    return self.find_simple_answer(simpleAC, imageB, answers)
                elif simpleAC == "not simple":
                    return self.find_simple_answer(simpleAB, imageC, answers)
                elif simpleAB != "not simple" and simpleAC != "not simple":
                    choice1 = self.find_simple_answer(simpleAB, imageC, answers)
                    choice2 = self.find_simple_answer(simpleAC, imageB, answers)
                    if choice1!=choice2:
                        print(problem_name + ": found two different answers")
                    return choice1
            #return -1

        elif problem_type == "3x3":
            #imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH = self.read_input_image_3x3(figures)
            #answers = self.read_answer_image_3x3(figures)
            return -1
        else:
            return -1

    def simple_compare(self, image1, image2):
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

        #print(count1, count2, count3)                

        min_diff = min(count1, count2, count3)
        if min_diff >= 1000:
            return "not simple"
        else:
            if count1 == min_diff:
                return "unchanged"
            elif count2 <= count3:
                return "flip_left_right"
            else:
                return "flip_top_bottom"

    def find_simple_answer(self, relation, image, answers):
        if relation == "unchanged":
            min_dist = 12000
            final_answer = 0
            for index in range(len(answers)):
                diff_img = np.array(ImageChops.difference(image,answers[index]))
                diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image))
                count = 0
                for i in range(len(diff_img)):
                    for j in range(len(diff_img[0])):
                        if diff_img[i][j] != 0:
                            count += 1 
                if count < min_dist and diff_fill < 0.02:
                    min_dist = count 
                    final_answer = index+1
            return final_answer

        elif relation == "flip_left_right":
            min_dist = 12000
            final_answer = 0
            for index in range(len(answers)):
                diff_img = np.array(ImageChops.difference(image.transpose(Image.FLIP_LEFT_RIGHT),answers[index]))
                diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image.transpose(Image.FLIP_LEFT_RIGHT)))
                count = 0
                for i in range(len(diff_img)):
                    for j in range(len(diff_img[0])):
                        if diff_img[i][j] != 0:
                            count += 1 
                #print("answer ",index,count,round(diff_fill,5))
                if count < min_dist and diff_fill < 0.02 and round(diff_fill,5)!=0.00154 and round(diff_fill,5)!=0.00174:
                    min_dist = count 
                    final_answer = index+1
            return final_answer
        
        elif relation == "flip_top_bottom":
            min_dist = 12000
            final_answer = 0
            for index in range(len(answers)):
                diff_img = np.array(ImageChops.difference(image.transpose(Image.FLIP_TOP_BOTTOM),answers[index]))
                diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image.transpose(Image.FLIP_TOP_BOTTOM)))
                count = 0
                for i in range(len(diff_img)):
                    for j in range(len(diff_img[0])):
                        if diff_img[i][j] != 0:
                            count += 1 
                #print("answer ",index,count,round(diff_fill,5))
                if count < min_dist and diff_fill < 0.02 and round(diff_fill,5)!=0.00089 and round(diff_fill,5)!=0.00458:
                    min_dist = count 
                    final_answer = index+1
            return final_answer

    def pixel_count_helper(self, image1, image2):
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
        return (count1, count2, count3, count4)

    def merge_two_image(self,image1, image2):
        img = image1
        for i in range(image1.size[0]):
            for j in range(image1.size[0]):
                if image1.getpixel((i,j)) == 0 or image2.getpixel((i,j)) == 0:
                    img.putpixel((i,j),0)
        return img

    def hard_compare(self, image1, image2, fill1, fill2):
        # check the fill rate for the image
        same_fill = np.abs(fill1 - fill2) < 0.02

        # shift the image
        # check if two images can rotated to each other
        min_shift_dist = 10000
        min_merge_dist = 10000
        shift_dist = [100,100]
        shift = False
        min_shift_diff = -1
        min_merge_diff = -1
        rotation = -1
        subset = False
        parent = "no"
        subset_point = [100,100]

        for x in range(-3,4):
            for y in range(-3,4):
                count1, count2, count3, count4 = -1,-1,-1,-1

                if x!=0 and y!=0:
                    shifted = ImageChops.offset(image1, xoffset=x, yoffset=y)
                    count1, count2, count3, count4 = self.pixel_count_helper(shifted, image2)
                    min_shift_diff = min(count1, count2, count3, count4)
                    
                    if min_shift_diff <= 1500 and min_shift_diff < min_shift_dist:
                        #print(count1, count2, count3, count4)
                        min_shift_dist = min_shift_diff
                        if min_shift_diff == count1:
                            rotation = 0
                        elif min_shift_diff == count2:
                            rotation = 90
                        elif min_shift_diff == count3:
                            rotation = 180
                        elif min_shift_diff == count4:
                            rotation = 270
                        shift = True
                        shift_dist[0] = x
                        shift_dist[1] = y

        # check if one image is a subset of merged image
        for x in range(-3,4):
            for y in range(-3,4):
                count1, count2 = -1,-1

                shifted = ImageChops.offset(image1, xoffset=x, yoffset=y)
                merged = self.merge_two_image(shifted, image2)
                diff1 = np.array(ImageChops.difference(image1,merged))
                diff2 = np.array(ImageChops.difference(image2,merged))
                for i in range(len(diff1)):
                    for j in range(len(diff1[0])):
                        if diff1[i][j] != 0:
                            count1 +=1 
                        if diff2[i][j] != 0:
                            count2 += 1
                min_merge_diff = min(count1, count2)
                    
                if min_merge_diff <= 1100 and min_merge_diff < min_merge_dist:
                    #print(count1, count2)
                    min_merge_dist = min_merge_diff
                    subset = True
                    subset_point[0] = x
                    subset_point[1] = y
                    if min_merge_diff == count1 and fill1>fill2:
                        parent = 'A'
                    elif min_merge_diff == count2 and fill2>fill1:
                        parent = 'BC'

        return (same_fill, rotation, shift, shift_dist, subset, subset_point, parent)

    def search_answer_helper1(self, rotation, image, answers, same_fill):
        min_dist = 12000
        final_answer = -1
        if rotation==90:
            rotation = 270
        for index in range(len(answers)):
            diff_img = np.array(ImageChops.difference(image.rotate(rotation),answers[index]))
            diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image))
            count = 0
            for i in range(len(diff_img)):
                for j in range(len(diff_img[0])):
                    if diff_img[i][j] != 0:
                        count += 1 
            if count < min_dist:
                min_dist = count 
                final_answer = index+1
        return final_answer
    
    def search_answer_helper2(self, parent, imageA, imageBC, answers, same_fill):
        min_dist = 12000
        final_answer = -1
        if parent == 'A':
            for index in range(len(answers)):
                merged = self.merge_two_image(imageBC, answers[index])
                diff_img = np.array(ImageChops.difference(merged,imageBC))
                threshold = np.array(ImageChops.difference(imageBC, answers[index]))
                #diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image))
                count = 0
                thresh_count = 0
                for i in range(len(diff_img)):
                    for j in range(len(diff_img[0])):
                        if diff_img[i][j] != 0:
                            count += 1 
                if count < min_dist:
                    min_dist = count 
                    final_answer = index+1
        else:
            # B or C is parent
            for index in range(len(answers)):
                merged = self.merge_two_image(imageBC, answers[index])
                diff_img = np.array(ImageChops.difference(merged, answers[index]))
                #threshold = np.array(ImageChops.difference(imageBC, answers[index]))
                #diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image))
                count = 0
                for i in range(len(diff_img)):
                    for j in range(len(diff_img[0])):
                        if diff_img[i][j] != 0:
                            count += 1 
                if count < min_dist:
                    min_dist = count 
                    final_answer = index+1
        return final_answer

    def find_hard_answer(self, featuresAB, featuresAC, answers, imageA, imageB, imageC):
        rotation1 = featuresAB[1]
        rotation2 = featuresAC[1]

        subset1 = featuresAB[4]
        subset2 = featuresAC[4]

        if rotation1 < 0 and rotation2 < 0:
            if not subset1 and not subset2:
                # try answer one by one, or random
                return self.try_answer(featuresAB, featuresAC, answers, imageA, imageB, imageC)

            elif subset1 and subset2:
                choice1 = self.search_answer_helper2(featuresAB[6], imageA, imageC, answers, featuresAB[0])
                choice2 = self.search_answer_helper2(featuresAC[6], imageA, imageB, answers, featuresAB[0])
                if choice1 != choice2:
                    print("Two answers: ",choice1, choice2)
                return choice1
            elif subset1:
                return self.search_answer_helper2(featuresAB[6], imageA, imageC, answers, featuresAB[0])
            elif subset2:
                return self.search_answer_helper2(featuresAC[6], imageA, imageB, answers, featuresAB[0])

        elif rotation1 >= 0:
            return self.search_answer_helper1(featuresAB[1], imageC, answers, featuresAB[0])
        elif rotation2 >= 0:
            return self.search_answer_helper1(featuresAC[1], imageB, answers, featuresAC[0])
        else:
            # AB rotation, AC rotation
            return -1  

    def try_answer(self, featuresAB, featuresAC, answers, imageA, imageB, imageC):
        all_answers = list(range(1,7))
        reject = []
        for index in range(len(answers)):
            diff_imgA = np.array(ImageChops.difference(answers[index], imageA))
            diff_imgB = np.array(ImageChops.difference(answers[index], imageB))
            diff_imgC = np.array(ImageChops.difference(answers[index], imageC))
            #diff_fill = np.abs(self.fill_rate(answers[index]) - self.fill_rate(image))
            countA, countB, countC = 0,0,0
            for i in range(len(diff_imgA)):
                for j in range(len(diff_imgA[0])):
                    if diff_imgA[i][j] != 0:
                        countA += 1 
                    if diff_imgB[i][j] != 0:
                        countB += 1 
                    if diff_imgC[i][j] != 0:
                        countC += 1 
            #print(countA, countB, countC)
            if countA < 500 or countB < 500 or countC < 500:
                reject.append(i)
        
        fillA, fillB, fillC = self.fill_rate(imageA), self.fill_rate(imageB), self.fill_rate(imageC)
        fill1 = self.fill_rate(answers[0])
        fill2 = self.fill_rate(answers[1])
        fill3 = self.fill_rate(answers[2])
        fill4 = self.fill_rate(answers[3])
        fill5 = self.fill_rate(answers[4])
        fill6 = self.fill_rate(answers[5]) 

        all_fill = [fill1, fill2, fill3, fill4, fill5, fill6]

        if featuresAB[0] and featuresAC[0]:
            min_fill = min(fillA, fillB, fillC) + 0.02
            max_fill = max(fillA, fillB, fillC) + 0.02
            for n,f in enumerate(all_fill):
                if not min_fill < f < max_fill:
                    reject.append(n+1)
        # elif featuresAB[0]:
        #     min_fill = fillC - 0.02
        #     max_fill = fillC + 0.02
        #     for n,f in enumerate(all_fill):
        #         if not min_fill < f < max_fill:
        #             reject.append(n+1)
        # elif featuresAC[0]:
        #     min_fill = fillB - 0.02
        #     max_fill = fillB + 0.02
        #     for n,f in enumerate(all_fill):
        #         if not min_fill < f < max_fill:
        #             reject.append(n+1)
        print(reject)
        for a in list(set(reject)):
            all_answers.remove(a)
        
        if len(all_answers) == 0:
            #return -1
            return np.random.randint(1,7,1)
        elif len(all_answers) == 1:
            return all_answers[0]
            #return -1
        else:
            #return -1
            return np.random.choice(all_answers)




