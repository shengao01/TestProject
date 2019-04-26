
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        valCurr = l1.val + l2.val
        up = valCurr / 10
        prevNode = answerNode = ListNode(valCurr % 10)
        l1 = l1.next
        l2 = l2.next
        while l1 is not None and l2 is not None:
            valCurr = l1.val + l2.val + up
            up = valCurr / 10
            nextNode = ListNode(valCurr % 10)
            prevNode.next = nextNode
            prevNode = nextNode
            l1 = l1.next
            l2 = l2.next
        followingNode = None
        if l1 is not None: followingNode = l1
        if l2 is not None: followingNode = l2
        while up != 0 and followingNode is not None:
            valCurr = up + followingNode.val
            up = valCurr / 10
            nextNode = ListNode(valCurr % 10)
            prevNode.next = nextNode
            prevNode = nextNode
            followingNode = followingNode.next
        if up != 0 and followingNode is None:
            nextNode = ListNode(up)
            prevNode.next = nextNode
            prevNode = nextNode
        if up == 0 and followingNode is not None:
            while followingNode is not None:
                nextNode = ListNode(followingNode.val)
                prevNode.next = nextNode
                prevNode = nextNode
                followingNode = followingNode.next
        return answerNode
