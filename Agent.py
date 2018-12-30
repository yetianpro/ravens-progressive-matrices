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

    def fill_rate(self, image):
        pixels = np.array(image)
        count, white = 0,0

        for i in range(len(pixels)):
            for j in range(len(pixels[0])):
                count += 1
                if pixels[i][j] == 0 :
                    white +=1
        rate = float(count - white) / count
        return round((1-rate) * 100, 3)

    def dark_rate(self, image):
        count, dark = 0,0
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                count += 1
                if image.getpixel((i, j)) == 0:
                    dark += 1
        rate = float(dark) / count
        return round(rate * 100, 3)

    def intersection_rate(self, image1, image2, image3):
        count = 0
        dark1, dark2, dark3 = 0, 0, 0
        merge = self.mergeThreeImage(image1, image2, image3)
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if merge.getpixel((i, j)) < 200:
                    count += 1
                if image1.getpixel((i, j)) < 200:
                    dark1 += 1
                if image2.getpixel((i, j)) < 200:
                    dark2 += 1
                if image3.getpixel((i, j)) < 200:
                    dark3 += 1
        rate1 = round(float(dark1) / count * 100, 3)
        rate2 = round(float(dark2) / count * 100, 3)
        rate3 = round(float(dark3) / count * 100, 3)
        return [rate1, rate2, rate3]

    def darkRateSameInGroup(self, image1, image2, image3, diffThreshold):

        dark_rates = sorted([self.dark_rate(image1), self.dark_rate(image2), self.dark_rate(image3)])

        diff1 = abs(dark_rates[0] - dark_rates[1])
        diff2 = abs(dark_rates[2] - dark_rates[1])
        diff3 = abs(dark_rates[0] - dark_rates[2])

        if diff1 < diffThreshold and diff2 < diffThreshold and diff3 < diffThreshold:
            return True
        return False

    def sortByDarkRate(self, group):
        rate1 = self.dark_rate(group[0])
        rate2 = self.dark_rate(group[1])
        rate3 = self.dark_rate(group[2])

        if rate1 >= rate2 >= rate3:
            return group
        if rate1 >= rate3 >= rate2:
            return [group[0], group[2], group[1]]
        if rate2 >= rate1 >= rate3:
            return [group[1], group[0], group[2]]
        if rate2 >= rate3 >= rate1:
            return [group[1], group[2], group[0]]
        if rate3 >= rate1 >= rate2:
            return [group[2], group[0], group[1]]
        if rate3 >= rate2 >= rate1:
            return [group[2], group[1], group[0]]

    def intersectionPatternBetweenRow(self, imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH):

        threshold = 5
        rowMatch, colMatch = False, False

        row1 = self.intersection_rate(imageA, imageB, imageC)
        row2 = self.intersection_rate(imageD, imageE, imageF)

        col1 = self.intersection_rate(imageA, imageD, imageG)
        col2 = self.intersection_rate(imageB, imageE, imageH)
        print("intersection test,", row1, row2, col1, col2)
        if abs(row1[0] - row2[0]) < threshold and abs(row1[1] - row2[1]) < threshold and abs(row1[2] - row2[2]) < threshold:
            rowMatch = True
        if abs(col1[0] - col2[0]) < threshold and abs(col1[1] - col2[1]) < threshold and abs(col1[2] - col2[2]) < threshold:
            colMatch = True

        if rowMatch:
            type = "row"
            result = self.findByIntersection(type, imageG, imageH, )
        if colMatch:
            type = "col"
            result = self.findByIntersection(type, imageC, imageF, )

        return -1



    def isGroupMerged(self, image1, image2, image3, threshold):
        if self.isMerged(image1, image2, image3,threshold) or self.isMerged(image1, image3, image2,threshold) or self.isMerged(image2,image3,image1,threshold):
            return True
        return False

    def findThirdMergedAnswer(self, image1, image2, answers):
        result = []

        for index, answer in enumerate(answers):
            if self.isGroupMerged(image1, image2, answer,1000):
                result.append(index + 1)
        #print(result)
        if len(result) == 1:
            return result[0]

        if len(result) > 1:
            result_copy = list(result)
            for possible_answer in result_copy:
                #print("compare answer", possible_answer)
                if self.isTwoSameNew(answers[possible_answer - 1], image1, 500):
                    if possible_answer in result:
                        result.remove(possible_answer)
                if self.isTwoSameNew(answers[possible_answer - 1], image2, 500):
                    if possible_answer in result:
                        result.remove(possible_answer)
        if len(result) == 1:
            return result[0]
        return -1

    def isSubsetGroup(self, image1, image2, image3):

        group = self.sortByDarkRate([image1, image2, image3])
        subset1 = self.isTwoSameNew(self.mergeTwoImage(group[0], group[1]), group[0], 1000)
        subset2 = self.isTwoSameNew(self.mergeTwoImage(group[0], group[2]), group[0], 1000)

        if subset1 and subset2:
            return True
        return False

    def findThirdSubsetAnswer(self, image1, image2, answers, inputs):
        result = []

        for index, answer in enumerate(answers):
            #print(index)
            if self.isSubsetGroup(image1, image2, answer):
                result.append(index + 1)

        if len(result) == 1:
            return result[0]

        if len(result) > 1:
            result_copy = list(result)
            for possible_answer in result_copy:
                for input in inputs:
                    if self.isTwoSameNew(answers[possible_answer-1], input, 1000):
                        result.remove(possible_answer)
                        break

        if len(result) == 1:
            return result[0]
        return -1

    def findBySameDark(self, range, answers):
        result = []
        for index, image in enumerate(answers):
            dark = self.dark_rate(image)
            if range[0] <= dark <= range[1]:
                result.append(index + 1)
        if len(result) == 1:
            return result[0]
        return -1

    def mergeTwoImage(self, image1, image2):
        img = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image1.getpixel((i, j)) < 200 or image2.getpixel((i, j)) < 200:
                    img.putpixel((i, j), 0)
        return img

    def isMerged(self, image1, image2, image3, threshold):
        merged = self.mergeTwoImage(image1, image2)
        if self.isTwoSame(merged, image3, threshold):
            return True
        return False

    def findExactAnswer(self, inputImage, answers):
        min_count = 10000
        result = -1
        for index, image in enumerate(answers):
            count = 0
            diff = np.array(ImageChops.difference(inputImage, image))
            for i in range(len(diff)):
                for j in range(len(diff[0])):
                    if diff[i][j] != 0:
                        count += 1
            if count < min_count:
                min_count = count
                result = index + 1
        return result

    def findMergedByTwo(self, image1, image2, answers):
        merged = self.mergeTwoImage(image1, image2)
        return self.findExactAnswer(merged, answers)

    def findMergedByFour(self, image1, image2, image3, image4, answers):
        merged1 = self.mergeTwoImage(image1, image2)
        merged2 = self.mergeTwoImage(image1, image2)
        merged3 = self.mergeTwoImage(merged1, merged2)
        return self.findExactAnswer(merged3, answers)

    def isTwoSame(self, image1, image2, threshold):
        count = 0
        diff = np.array(ImageChops.difference(image1,image2))
        for i in range(len(diff)):
            for j in range(len(diff[0])):
                if diff[i][j] != 0:
                    count +=1
        #print(count)
        if count <= threshold:
            return True
        return False

    def isTwoSameNew(self, image1, image2, threshold):
        count,same = 0, 0
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                count += 1
                if (image1.getpixel((i, j)) < 200 and image2.getpixel((i, j)) < 200) or (image1.getpixel((i, j)) >= 200 and image2.getpixel((i, j)) >=200) :
                    same += 1
        if count-same <= threshold:
            return True
        return False

    def isThreeSame(self, image1, image2, image3):
        if self.isTwoSame(image1, image2, 1500) and self.isTwoSame(image2, image3, 1500) and self.isTwoSame(image1,image3, 1500):
            return True
        return False

    def findGroups(self, inputs):
        all = list(range(8))
        result = []
        for i in range(len(inputs)):
            for j in range(i+1, len(inputs)):
                for k in range(j+1, len(inputs)):
                    if i not in result and j not in result and k not in result:
                        if self.isThreeSame(inputs[i], inputs[j], inputs[k]):
                            result.append(i)
                            result.append(j)
                            result.append(k)
        if len(result) > 0:
            for item in result:
                all.remove(item)
            return all
        return []

    def findThirdSimilarAnswer(self, groups, inputs, answers):
        image1 = inputs[groups[0]]
        image2 = inputs[groups[1]]
        result = []
        for index,image in enumerate(answers):
            if self.isTwoSame(image1, image, 600) or self.isTwoSame(image2, image, 600):
                #print("answer:", index+1)
                result.append(index+1)
        return result

    def isImageAnd(self, image1, image2, image3):
        imgAnd = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgAnd.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) == 0:
                    imgAnd.putpixel((i, j), 0)

        return self.isTwoSame(image3, imgAnd, 500)

    def findImageAndByTwo(self, image1, image2, answers):
        imgAnd = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgAnd.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) == 0:
                    imgAnd.putpixel((i, j), 0)

        return self.findExactAnswer(imgAnd, answers)

    def findImageAndByFour(self, image1, image2, image3, image4, answers):
        imgAnd = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgAnd.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) == 0:
                    imgAnd.putpixel((i, j), 0)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image3.getpixel((i, j)) == 0 and image4.getpixel((i, j)) == 0:
                    imgAnd.putpixel((i, j), 0)

        return self.findExactAnswer(imgAnd, answers)

    def isImageXOR(self, image1, image2, image3):
        imgXOR = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgXOR.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if (image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) != 0) or (
                        image1.getpixel((i, j)) != 0 and image2.getpixel((i, j)) == 0):
                    imgXOR.putpixel((i, j), 0)
        return self.isTwoSame(image3, imgXOR, 2000)

    def findImageXORByTwo(self, image1, image2, answers):
        imgXOR = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgXOR.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if (image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) != 0) or (
                        image1.getpixel((i, j)) != 0 and image2.getpixel((i, j)) == 0):
                    imgXOR.putpixel((i, j), 0)

        return self.findExactAnswer(imgXOR, answers)

    def findImageXORByFour(self, image1, image2, image3, image4, answers):
        imgXOR = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                imgXOR.putpixel((i, j), 255)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if (image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) != 0) or (
                        image1.getpixel((i, j)) != 0 and image2.getpixel((i, j)) == 0):
                    imgXOR.putpixel((i, j), 0)

        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if (image1.getpixel((i, j)) == 0 and image2.getpixel((i, j)) != 0) or (
                        image1.getpixel((i, j)) != 0 and image2.getpixel((i, j)) == 0):
                    imgXOR.putpixel((i, j), 0)

        return self.findExactAnswer(imgXOR, answers)

    def findByRateRange(self, range, inputs ,answers):
        result = []
        for index, image in enumerate(answers):
            dark = self.dark_rate(image)
            if range[0] <= dark <= range[1]:
                result.append(index + 1)

        if len(result) > 1:
            result_copy = list(result)
            for possible_answer in result_copy:
                for input in inputs:
                    if self.isTwoSame(answers[possible_answer-1], input, 500):
                        result.remove(possible_answer)
                        break
        return result

    def darkRateSumA(self, imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            inputs, answers):

        findThreshold = 0.4
        answerThreshold = 0.2

        rowMatch, colMatch = False, False

        darkA = self.dark_rate(imageA)
        darkB = self.dark_rate(imageB)
        darkC = self.dark_rate(imageC)
        darkD = self.dark_rate(imageD)
        darkE = self.dark_rate(imageE)
        darkF = self.dark_rate(imageF)
        darkG = self.dark_rate(imageG)
        darkH = self.dark_rate(imageH)

        if abs(darkA - abs(darkB + darkC)) < findThreshold and abs(darkD - abs(darkE + darkF)) < findThreshold:
            rowMatch = True
        if abs(darkA - abs(darkD + darkG)) < findThreshold and abs(darkB - abs(darkE + darkH)) < findThreshold:
            colMatch = True

        if rowMatch and colMatch:
            rowRateRange = [darkG - darkH - answerThreshold, darkG - darkH + answerThreshold]
            colRateRange = [darkC - darkF - answerThreshold, darkC - darkF + answerThreshold]
            answerRange = [min(rowRateRange[0],colRateRange[0]), max(rowRateRange[1],colRateRange[1])]
            possibles = self.findByRateRange(answerRange, inputs ,answers)

            if len(possibles) == 1:
                return possibles[0]

        if rowMatch:
            answerRange = [darkG - darkH - answerThreshold, darkG - darkH + answerThreshold]
            possibles = self.findByRateRange(answerRange, inputs ,answers)

            if len(possibles) == 1:
                return possibles[0]

        if colMatch:
            answerRange = [darkC - darkF - answerThreshold, darkC - darkF + answerThreshold]
            possibles = self.findByRateRange(answerRange, inputs, answers)

            if len(possibles) == 1:
                return possibles[0]

        return -1

    def mergeThreeImage(self, image1, image2, image3):
        img = image1.copy()
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                if image1.getpixel((i, j)) < 200 or image2.getpixel((i, j)) < 200 or image3.getpixel((i, j)) < 200:
                    img.putpixel((i, j), 0)
        return img

    def findBySumImage(self, sum, image1, image2, answers, inputs, threshold):
        result = []
        for index, image in enumerate(answers):
            merge = self.mergeThreeImage(image1, image2, image)
            if self.isTwoSame(merge, sum, threshold):
                result.append(index + 1)
        #print(result)
        if len(result) > 1:
            result_copy = list(result)
            for possible_answer in result_copy:
                for input in inputs:
                    if self.isTwoSame(answers[possible_answer-1], input, 1000):
                        result.remove(possible_answer)
                        break

        return result

    def darkRateFixedSum(self, imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            inputs, answers):
        row1 = self.mergeThreeImage(imageA, imageB, imageC)
        row2 = self.mergeThreeImage(imageD, imageE, imageF)

        col1 = self.mergeThreeImage(imageA, imageD, imageG)
        col2 = self.mergeThreeImage(imageB, imageE, imageH)

        rowSame, colSame = False, False

        if self.isTwoSame(row1, row2, 1000):
            rowSame = True
        if self.isTwoSame(col1, col2, 1000):
            colSame = True

        #print("pattern", rowSame, colSame)

        if rowSame:
            possibles = self.findBySumImage(row1,imageG,imageH, answers, inputs, 1000)
            #print("row", possibles)
            if len(possibles) == 1:
                return possibles[0]
        if colSame:
            possibles = self.findBySumImage(col1,imageC,imageF, answers, inputs, 1000)
            #print("col", possibles)
            if len(possibles) == 1:
                return possibles[0]
        return -1

    def commonInTwoImage(self, image1, image2):
        count, common = 0, 0
        for i in range(image1.size[0]):
            for j in range(image1.size[1]):
                count += 1
                if (image1.getpixel((i, j)) < 200 and image2.getpixel((i, j)) < 200) or (image1.getpixel((i, j)) >= 200 and image2.getpixel((i, j)) >= 200):
                    common += 1
        return common

    def darkRateCommon(self, imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            inputs, answers):

        threshold = 500

        row1 = [self.commonInTwoImage(imageA, imageB),self.commonInTwoImage(imageB, imageC)]
        row2 = [self.commonInTwoImage(imageD, imageE),self.commonInTwoImage(imageE, imageF)]

        col1 = [self.commonInTwoImage(imageA, imageD),self.commonInTwoImage(imageD, imageG)]
        col2 = [self.commonInTwoImage(imageB, imageE),self.commonInTwoImage(imageE, imageH)]

        row1Same, row2Same, col1Same, col2Same = False, False, False, False

        if abs(row1[0] - row1[1]) < threshold:
            row1Same = True
        if abs(row2[0] - row2[1]) < threshold:
            row2Same = True
        if abs(col1[0] - col1[1]) < threshold:
            col1Same = True
        if abs(col2[0] - col2[1]) < threshold:
            col2Same = True

        if row1Same and row2Same:
            possibles = self.findByCommon(imageG,imageH, answers, inputs, 500)
            #print("row", possibles)
            if len(possibles) == 1:
                return possibles[0]
        if col1Same and col2Same:
            possibles = self.findByCommon(imageC,imageF, answers, inputs, 500)
            #print("col", possibles)
            if len(possibles) == 1:
                return possibles[0]
        return -1

    def findByCommon(self, image1, image2, answers, inputs, threshold):
        target = self.commonInTwoImage(image1, image2)
        result = []
        for index, image in enumerate(answers):
            common = self.commonInTwoImage(image2, image)
            if abs(common - target) < threshold:
                result.append(index + 1)
        #print(result)
        if len(result) > 1:
            result_copy = list(result)
            for possible_answer in result_copy:
                for input in inputs:
                    if self.isTwoSameNew(answers[possible_answer-1], input, 500):
                        result.remove(possible_answer)
                        break
        return result





    def find_flip(self, image1, image2):
        count1, count2, count3 = 0, 0, 0

        diff1 = np.array(ImageChops.difference(image1, image2))
        diff2 = np.array(ImageChops.difference(image1.transpose(Image.FLIP_LEFT_RIGHT), image2))
        diff3 = np.array(ImageChops.difference(image1.transpose(Image.FLIP_TOP_BOTTOM), image2))

        for i in range(len(diff1)):
            for j in range(len(diff1[0])):
                if diff1[i][j] != 0:
                    count1 += 1
                if diff2[i][j] != 0:
                    count2 += 1
                if diff3[i][j] != 0:
                    count3 += 1

        min_diff = min(count2, count3)
        # print(count2,count3)
        if min_diff >= 790:
            return (False, "not flip")
        else:
            if count2 <= count3:
                return (True, "flip_left_right")
            else:
                return (True, "flip_top_bottom")

    def find_rotation(self, image1, image2):
        count1, count2, count3, count4 = 0, 0, 0, 0

        diff1 = np.array(ImageChops.difference(image1, image2))
        diff2 = np.array(ImageChops.difference(image1.rotate(90), image2))
        diff3 = np.array(ImageChops.difference(image1.rotate(180), image2))
        diff4 = np.array(ImageChops.difference(image1.rotate(270), image2))

        for i in range(len(diff1)):
            for j in range(len(diff1[0])):
                if diff1[i][j] != 0:
                    count1 += 1
                if diff2[i][j] != 0:
                    count2 += 1
                if diff3[i][j] != 0:
                    count3 += 1
                if diff4[i][j] != 0:
                    count4 += 1
        min_diff = min(count2, count3, count4)
        print(count2, count3, count4)
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

    def guessByRemoveInput(self,imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            answers):
        possible_answers = [1,2,3,4,5,6,7,8]
        threshold = 1000
        answers_copy = list(answers)
        for index,value in enumerate(answers_copy):
            if self.isTwoSameNew(imageA, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageB, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageC, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageD, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageE, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageF, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageG, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
            if self.isTwoSameNew(imageH, value, threshold):
                try:
                    possible_answers.remove(index + 1)
                except:
                    pass
        return possible_answers


    def Solve(self,problem):
        global problem_name
        problem_type = problem.problemType
        problem_name = problem.name
        #problem_diffcult = problem.name.split()[0]
        figures = problem.figures

        if problem_type == "3x3":

            imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH = self.read_input_image_3x3(figures)
            inputs = (imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH)
            answer1,answer2,answer3,answer4,answer5,answer6,answer7,answer8 = self.read_answer_image_3x3(figures)
            answers = (answer1,answer2,answer3,answer4,answer5,answer6,answer7,answer8)

            #print(problem_name)

            # test purpose
            # if problem_name in ["Basic Problem D-08"]:
            #     print(problem_name)
            #     return -1
            # else:
            #     return -1


            input_fill_rates = [self.fill_rate(imageA),self.fill_rate(imageB),
                                self.fill_rate(imageC),self.fill_rate(imageD),
                                self.fill_rate(imageE),self.fill_rate(imageF),
                                self.fill_rate(imageG),self.fill_rate(imageH)]

            answer_fill_rates = [self.fill_rate(answer1),self.fill_rate(answer2),
                                 self.fill_rate(answer3),
                                 self.fill_rate(answer4),self.fill_rate(answer5),self.fill_rate(answer6),
                                 self.fill_rate(answer7),self.fill_rate(answer8)]

            # find same image groups
            groups = self.findGroups(inputs)
            if len(groups) == 2:
                result = self.findThirdSimilarAnswer(groups, inputs, answers)
                if len(result) ==1:
                    print(problem_name, "find by similar groups:", result[0])
                    return result[0]


            # merged by row and column, from left to right
            rowAdd, colAdd = False, False
            rowFillAdd, colFillAdd = False, False

            if self.isMerged(imageA, imageB, imageC, 1000) or self.isMerged(imageD, imageE, imageF, 1000):
                rowAdd = True
            if self.isMerged(imageA, imageD, imageG, 1000) or self.isMerged(imageB, imageE, imageH, 1000):
                colAdd = True

            if input_fill_rates[2] > input_fill_rates[1] and input_fill_rates[2] > input_fill_rates[0] and input_fill_rates[5] > input_fill_rates[3] and input_fill_rates[5] > input_fill_rates[4]:
                rowFillAdd = True

            if input_fill_rates[2] > input_fill_rates[1] and input_fill_rates[2] > input_fill_rates[0] and input_fill_rates[5] > input_fill_rates[3] and input_fill_rates[5] > input_fill_rates[4]:
                colFillAdd = True

            if rowAdd and colAdd and rowFillAdd and colFillAdd:
                result = self.findMergedByFour(imageC, imageF, imageG, imageH, answers)
                print(problem_name, "both merged -->:", result)
                return result
            if rowAdd and rowFillAdd:
                result = self.findMergedByTwo(imageG, imageH, answers)
                print(problem_name, "row merged -->:", result)
                return result
            if colAdd and colFillAdd:
                result = self.findMergedByTwo(imageC, imageF, answers)
                print(problem_name, "col merged -->:", result)
                return result

            # image XOR by row and column
            rowXOR, colXOR = False, False

            if self.isImageXOR(imageA, imageB, imageC) and self.isImageXOR(imageD, imageE, imageF):
                rowXOR = True
            if self.isImageXOR(imageA, imageD, imageG) and self.isImageXOR(imageB, imageE, imageH):
                colXOR = True

            if rowXOR and colXOR:
                result = self.findImageXORByFour(imageC, imageF, imageG, imageH, answers)
                print(problem_name, "both XOR -->:", result)
                return result
            if rowXOR:
                result = self.findImageXORByTwo(imageG, imageH, answers)
                print(problem_name, "row XOR -->:", result)
                return result
            if colXOR:
                result = self.findImageXORByTwo(imageC, imageF, answers)
                print(problem_name, "col XOR -->:", result)
                return result


            # image AND by row and column
            rowAnd, colAnd = False, False

            if self.isImageAnd(imageA, imageB, imageC) and self.isImageAnd(imageD, imageE, imageF):
                rowAnd = True
            if self.isImageAnd(imageA, imageD, imageG) and self.isImageAnd(imageB, imageE, imageH):
                colAnd = True

            if rowAnd and colAnd:
                result = self.findImageAndByFour(imageC, imageF, imageG, imageH, answers)
                print(problem_name, "both and -->:", result)
                return result
            if rowAnd:
                result = self.findImageAndByTwo(imageG, imageH, answers)
                print(problem_name, "row and -->:", result)
                return result
            if colAnd:
                result = self.findImageAndByTwo(imageC, imageF, answers)
                print(problem_name, "col and -->:", result)
                return result

            # dark rate A=B+C, A=D+G
            result = self.darkRateSumA(imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            inputs, answers)
            if result != -1:
                print(problem_name, "dark sum A:", result)
                return result

            # dark rate fixed sum in row or column, A+B+C = D+E+F, A+D+G = B+E+H
            result = self.darkRateFixedSum(imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,
            inputs, answers)
            if result != -1:
                print(problem_name, "fixed sum rate in row or col:", result)
                return result

            # dark rate fixed subtraction
            result = self.darkRateCommon(imageA, imageB, imageC, imageD, imageE, imageF, imageG, imageH,
                                           inputs, answers)
            if result != -1:
                print(problem_name, "fixed common rate in row or col:", result)
                return result

            # dark rate same in group A=E=# , B=F=G , C=D=H
            darkGroup1 = self.darkRateSameInGroup(imageB, imageF, imageG, 1)
            darkGroup2 = self.darkRateSameInGroup(imageC, imageD, imageH, 1)

            if darkGroup1 and darkGroup2:
                range = [min(self.dark_rate(imageA), self.dark_rate(imageE)) - 1,
                         max(self.dark_rate(imageA), self.dark_rate(imageE)) + 1]
                result = self.findBySameDark(range, answers)
                if result != -1:
                    print(problem_name, "AE# dark rate", result)
                    return result

            # dark rate same in group C=E=G , A=F=H, B=D=#
            darkGroup1 = self.darkRateSameInGroup(imageC, imageE, imageG, 1)
            darkGroup2 = self.darkRateSameInGroup(imageA, imageF, imageH, 1)

            if darkGroup1 == 'all same' and darkGroup2 == 'all same':
                range = [min(self.dark_rate(imageB), self.dark_rate(imageD)) - 1,
                         max(self.dark_rate(imageB), self.dark_rate(imageD)) + 1]
                result = self.findBySameDark(range, answers)
                if result != -1:
                    print(problem_name, "BD# dark rate:", result)
                    return result

            # dark rate same in group row, A=B=C, D=E=F
            darkGroup1 = self.darkRateSameInGroup(imageA, imageB, imageC, 1)
            darkGroup2 = self.darkRateSameInGroup(imageD, imageE, imageF, 1)

            if darkGroup1 == 'all same' and darkGroup2 == 'all same':
                range = [min(self.dark_rate(imageG), self.dark_rate(imageH)) - 1,
                         max(self.dark_rate(imageG), self.dark_rate(imageH)) + 1]
                result = self.findBySameDark(range, answers)
                if result != -1:
                    print(problem_name, "row dark rate:", result)
                    return result

            # dark rate in group column A=D=G, B=E=H
            darkGroup1 = self.darkRateSameInGroup(imageA, imageD, imageG, 1)
            darkGroup2 = self.darkRateSameInGroup(imageB, imageE, imageH, 1)

            if darkGroup1 == 'all same' and darkGroup2 == 'all same':
                range = [min(self.dark_rate(imageC), self.dark_rate(imageF)) - 1,
                         max(self.dark_rate(imageC), self.dark_rate(imageF)) + 1]
                result = self.findBySameDark(range, answers)
                if result != -1:
                    print(problem_name, "col dark rate:", result)
                    return result


            # intersection with between group row or col


            # intersection with between group AE#, BFG, CDH


            # intersection with between group CEG, AFH, BD#




            # merged AE#, BFG, CDH
            group1Merged = self.isGroupMerged(imageB, imageF, imageG, 1500)
            group2Merged = self.isGroupMerged(imageC, imageD, imageH, 1500)

            if group1Merged and group2Merged:
                result = self.findThirdMergedAnswer(imageA, imageE, answers)
                if result != -1:
                    print(problem_name, "AE# merged:", result)
                    return result

            # merged CEG, AFH, BD#
            group1Merged = self.isGroupMerged(imageC, imageE, imageG, 1500)
            group2Merged = self.isGroupMerged(imageA, imageF, imageH, 1500)

            if group1Merged and group2Merged:
                result = self.findThirdMergedAnswer(imageB, imageD, answers)
                if result != -1:
                    print(problem_name, "BD# merged:", result)
                    return result

            # subset AE#, BFG, CDH
            subset1 = self.isSubsetGroup(imageB, imageF, imageG)
            subset2 = self.isSubsetGroup(imageC, imageD, imageH)

            if subset1 and subset2:
                result = self.findThirdSubsetAnswer(imageA, imageE, answers, inputs)
                if result != -1:
                    print(problem_name, "AE# subset:", result)
                    return result

            # subset CEG, AFH, BD#
            subset1 = self.isSubsetGroup(imageC, imageE, imageG)
            subset2 = self.isSubsetGroup(imageA, imageF, imageH)

            if subset1 and subset2:
                result = self.findThirdSubsetAnswer(imageB, imageD, answers, inputs)
                if result != -1:
                    print(problem_name, "BD# subset:", result)
                    return result

            # subset row
            subset1 = self.isSubsetGroup(imageA, imageB, imageC)
            subset2 = self.isSubsetGroup(imageD, imageE, imageF)

            if subset1 and subset2:
                result = self.findThirdSubsetAnswer(imageG, imageH, answers, inputs)
                if result != -1:
                    print(problem_name, "row subset:", result)
                    return result

            # subset col
            subset1 = self.isSubsetGroup(imageA, imageD, imageG)
            subset2 = self.isSubsetGroup(imageB, imageE, imageH)

            if subset1 and subset2:
                result = self.findThirdSubsetAnswer(imageC, imageF, answers, inputs)
                if result != -1:
                    print(problem_name, "col subset:", result)
                    return result

            # merged row
            group1Merged = self.isGroupMerged(imageA, imageB, imageC, 1500)
            group2Merged = self.isGroupMerged(imageD, imageE, imageF, 1500)

            if group1Merged and group2Merged:
                result = self.findThirdMergedAnswer(imageG, imageH, answers)
                if result != -1:
                    print(problem_name, "row merged:", result)
                    return result

            # merged col
            group1Merged = self.isGroupMerged(imageA, imageD, imageG, 1500)
            group2Merged = self.isGroupMerged(imageB, imageE, imageH, 1500)

            if group1Merged and group2Merged:
                result = self.findThirdMergedAnswer(imageC, imageF, answers)
                if result != -1:
                    print(problem_name, "col merged:", result)
                    return result


            # start other methods
            # fill rate analysis
            threshold = 0.35
            after_fill_rates = self.fill_rate_analysis(input_fill_rates, answer_fill_rates, threshold)
            if len(after_fill_rates) == 1:
                print(problem_name, "fill rate analysis", after_fill_rates[0])
                return after_fill_rates[0]

            # guess by remove exist input
            possibleAnswers = self.guessByRemoveInput(imageA,imageB,imageC,imageD,imageE,imageF,imageG,imageH,answers)
            # print("after remove", possibleAnswers)
            if len(possibleAnswers) == 1:
                print(problem_name, "remove input:", possibleAnswers[0])
                return possibleAnswers[0]

            if len(after_fill_rates) != 0:
                return np.random.choice(after_fill_rates)

            if len(possibleAnswers) !=0:
                return np.random.choice(possibleAnswers)

            return np.random.choice([1,2,3,4,5,6,7,8])
        else:
            return -1


