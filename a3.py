def merge(p,q):
    i= 0
    j= 0
    ans = []
    while i<len(p) and j<len(q):
        if p[i][1]>q[j][1]:
            ans.append(q[j])
            j+=1
        elif p[i][1]<q[j][1]:
            ans.append(p[i])
            i+=1
        else :
            ans.append(p[i])
            ans.append(q[j])
            i+=1
            j+=1
    if i==len(p):
        ans.extend(q[j:])
    elif j==len(q):
        ans.extend(p[i:])
    return ans

class xnode :
    def __init__(self,xrange):
        self.xrange = xrange
        self.ylist = []
        self.left = None
        self.right = None
        self.data = None

def xavl(pointlistx):
    if len(pointlistx)==0 :
        return None 
    median= len(pointlistx)//2
    n= len(pointlistx)
    if n==1 :
        node1= xnode([pointlistx[0][0],pointlistx[0][0]])
        node1.data= pointlistx[0]
        node1.ylist = [pointlistx[0]]
        return node1
    root = xnode([pointlistx[0][0],pointlistx[n-1][0]])
    root.left = xavl(pointlistx[0:median])
    root.right = xavl(pointlistx[median:])
    return root

def correct_avl(root):
    if root == None :
        return
    
    elif root.left == None and root.right == None :
        return 
    
    correct_avl(root.left)
    correct_avl(root.right)
    root.ylist = merge(root.left.ylist,root.right.ylist)

def phi(p1,p2):
    if p1[1]<p2[0] or p1[0]>p2[1]:
        return True
    return False 
def present(p1,p2):       #true if p1 in p2
    if p1[0]>=p2[0] and p1[1]<=p2[1]:
        return True
    return False

def searchhigh(arr,l,h,x):
    if l==h+1 or l==h :
        if arr[l][1]<x:
            return l+1
        else :
            return l
    mid =(l+h)//2
    if arr[mid][1]==x :
        return mid
    elif arr[mid][1] > x:
        return searchhigh(arr, l, mid - 1, x)
    else:
        return searchhigh(arr, mid + 1, h, x)



def searchlow(arr,l,h,x):
    if l==h+1 or l==h :
        if arr[l][1]>x:
            return l-1
        else :
            return l
    mid =(l+h)//2
    if arr[mid][1]==x :
        return mid
    elif arr[mid][1] > x:
        return searchlow(arr, l, mid - 1, x)
    else:
        return searchlow(arr, mid + 1, h, x)

def query_y(ylist,q,d):
    a=q[1]-d
    b=q[1]+d
    if len(ylist)==1 :
        if ylist[0][1]>=a and ylist[0][1]<=b :
            return [ylist[0]]
        else :
            return []
    else :
        i= searchhigh(ylist,0,len(ylist)-1,a)
        if i==len(ylist):
            return []
        j= searchlow(ylist,0,len(ylist)-1,b)
        if j<0:
            return []
        ans=[]
        for k in range(i,j+1):
            ans.append(ylist[k])
        return ans
        
def query(root, q,d):
    if root == None :
        return []
    x_req= [q[0]-d,q[0]+d]
    if present(root.xrange,x_req):
        return query_y(root.ylist,q,d)
    elif phi(root.xrange,x_req):
        return []
    else :
        return query(root.left,q,d)+query(root.right,q,d)
        
class PointDatabase:
    def __init__(self,pointlist=[]):
        #returns a list of range nodes (ie range tree) and root [in form of tuple]
        
        pointlist.sort()
        root = xavl(pointlist)
        correct_avl(root)
        self.root = root

    def searchNearby(self,q,d):
        root = self.root
        return query(root,q,d)


        
        








        
