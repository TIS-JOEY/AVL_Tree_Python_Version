class TreeNode:
    #data為此節點的值，left指向左子節點，right指向右子節點，parent指向父節點，factor為平衡數值
    def __init__(self,data,left = None,right = None,parent = None,factor = 0):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.factor = factor
    
    #判別是否為其父節點的左子節點
    def isLeftChild(self):
        return (self.parent and self.parent.left == self)
    
    #判別是否為其父節點的右子節點
    def isRightChild(self):
        return (self.parent and self.parent.right == self)
    
    #判別是否為有右子節點
    def hasRightChild(self):
        return self.right!=None
    
    #判別是否為有左子節點
    def hasLeftChild(self):
        return self.left!=None
    
    #判別是否為葉子節點
    def isLeaf(self):
        return not (self.left or self.right)

class AVL_Tree:
    def __init__(self):
        self.root = None
    
    def put(self,data):
        #若根節點為None，則可直接指定。
        if(self.root == None):
            self.root = TreeNode(data)
        
        #加入樹中的某位置，並調整平衡數值
        else:
            self._put(data,self.root)
    
    def _put(self,data,run_node):
        if(run_node.data > data):
            #要加入的數值比較小，要往左子樹走
            if(run_node.hasLeftChild()):
                self._put(data,run_node.left)
            
            #因為無左子節點，所以可以指定其左子節點為要加入的樹節點
            else:
                newNode = TreeNode(data)
                run_node.left = newNode
                newNode.parent = run_node
                #因新增一節點，所以要進行更新factor的動作
                self.update_factor(run_node.left)
                
        #要加入的數值比較大，要往右子樹走
        else:
            if(run_node.hasRightChild()):
                self._put(data,run_node.right)
            else:
                #因為無右子節點，所以可以指定其右子節點為要加入的樹節點
                newNode = TreeNode(data)
                run_node.right = newNode
                newNode.parent = run_node
                #因新增一節點，所以要進行更新factor的動作
                self.update_factor(run_node.right)
    
    def update_factor(self,check_node):
        #若檢查的節點平衡數值>1或<1則進行處理
        if(check_node.factor > 1 or check_node.factor < -1):
            self.rebalance(check_node)
            return
        
        if(check_node.parent):
            #若是其父節點的左子節點，則其父節點的平衡數值+1
            if(check_node.isLeftChild()):
                check_node.parent.factor+=1         
            #若是其父節點的右子節點，則其父節點的平衡數值-1
            else:
                check_node.parent.factor-=1
            
            #若其父節點的平衡數值已成為0，就代表不用再往上調整了，因為已經平衡了不會影響到上面的平衡數值
            if(check_node.parent!=0):
                self.update_factor(check_node.parent)
    
    def rotateLeft(self,old_node):
        #以原節點的右子節點來作為基準點
        new_node = old_node.right
        #將基準點的左子節點指定給原節點的右子節點，如此可以確保中序且避免節點衝突
        old_node.right = new_node.left
        #將基準點的父節點設為原節點的父節點
        new_node.parent = old_node.parent
        
        if new_node.left:
            #若基準點的左子節點是有節點的，則就要更新他的parent
            new_node.left.parent = old_node
        
        if self.root==old_node:
            #若原節點為根節點，則將基準點設為根節點
            self.root = new_node
        else:
            if(old_node.isLeftChild()):
                #若原節點為其父節點的左子節點，則必須將其父節點的左子節點設為基準點
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
            
        
        #將基準點的左子節點設為原節點
        new_node.left = old_node
        #將原節點的父節點設為基準點
        old_node.parent = new_node
        
        
        #進行factor的更新
        old_node.factor = old_node.factor +1 - min(0,new_node.factor)
        new_node.factor = new_node.factor +1 + max(0,old_node.factor)
    
    def rotateRight(self,old_node):
        #以原節點的左子節點來作為基準點
        new_node = old_node.left
        #將基準點的右子節點指定給原節點的左子節點，如此可以確保中序且避免節點衝突
        old_node.left = new_node.right
        #將基準點的父節點設為原節點的父節點
        new_node.parent = old_node.parent
        
        if new_node.right:
            #若基準點的左子節點是有節點的，則就要更新他的parent
            new_node.right.parent = old_node
        
        if self.root==old_node:
           #若原節點為根節點，則將基準點設為根節點
            self.root = new_node
            
        if old_node.parent:
            if old_node.isLeftChild():
                old_node.parent.left = new_node
            else:
                old_node.parent.right = new_node
            
        #將基準點的右子節點設為原節點
        new_node.right = old_node
        #將原節點的父節點設為基準點
        old_node.parent = new_node
        
        #進行factor的更新
        old_node.factor = old_node.factor -1 - max(new_node.factor,0)
        new_node.factor = new_node.factor -1 + min(old_node.factor,0)
        
    def rebalance(self,node):
        if(node.factor < 0):
            #R類型
            if(node.right.factor > 0):
                #RL類型，須先右轉再左轉
                self.rotateRight(node.right)
                self.rotateLeft(node)
            else:
                #RR類型，直接左轉
                self.rotateLeft(node)
        else:
            #L類型
            if(node.left.factor < 0):
                #LR類型，須先左轉再右轉
                self.rotateLeft(node.left)
                self.rotateRight(node)
            else:
                #LL類型，直接右轉
                self.rotateRight(node)
    
    def update_delete_facotr(self,run_node):
        #若檢查的節點平衡數值>1或<1則進行處理
        if run_node.factor < -1 or run_node.factor > 1:
            self.rebalance(run_node)
            return
        if run_node.parent:
            #若是其父節點的左子節點，則其父節點的平衡數值-1(因為是刪除)
            if(run_node.isLeftChild()):
                run_node.parent.factor-=1
            
            #若是其父節點的右子節點，則其父節點的平衡數值+1(因為是刪除)
            elif(run_node.isRightChild()):
                run_node.parent.factor+=1
            
            #若其父節點的平衡數值已成為0，就代表不用再往上調整了，因為已經平衡了不會影響到上面的平衡數值
            if run_node.parent.factor!=0:
                self.update_delete_facotr(run_node.parent)
    
    #中序排序
    def inorder(self,node):
        if node:
            self.inorder(node.left)
            print(node.data,node.factor)
            self.inorder(node.right)
    
    #前序排序
    def preorder(self,node):
        if node:
            print(node.data)
            self.preorder(node.left)
            self.preorder(node.right)
    
    def findLeftMin(self):
        run_node,pre_node = self.root,self.root
        while run_node.left != None and not run_node.isLeaf():
            run_node,pre_node = run_node.left,run_node
            
        #此時run_node為左子樹中最小值的節點，而pre_node為其父節點
        return run_node,pre_node
        
    
    def findRightMax(self):
        run_node,pre_node = self.root,self.root
        while run_node.right != None and not run_node.isLeaf():
            run_node,pre_node = run_node.right,run_node
            
        #此時run_node為右子樹中最大值的節點，而pre_node為其父節點
        return run_node,pre_node
    
    def delete(self,data):
        run_node = self.root
        
        while(run_node!=None):    
            #找到要被刪除的節點
            if(run_node.data == data):
                break
            
            #比要查找的值小，往右子樹跑
            elif(run_node.data > data):
                run_node = run_node.left
            
            #比要查找的數值大，往左子樹跑
            else:
                run_node = run_node.right
        
        #找不到要被刪除的節點
        if run_node == None: 
            return
        
        #若要刪除的節點為根節點
        if self.root == run_node:
            
            #若只剩一個根節點
            if(self.root.isLeaf()):
                self.root = None
            else:
                #找出左子樹中最小的數值來取代，以符合中序排列
                replace,replace_parent = self.findLeftMin()

                #進行取代
                run_node.data = replace.data
                
                #刪除左子樹最小值的節點
                replace_parent.left = None
                
                #因刪除所以要將左子樹最小值節點的父節點之平衡數值-1 (因為刪除的是左子節點)
                replace_parent.factor-=1 
                
                #若所找到的最小數值為根節點，就代表了根節點已經沒有左子樹了，這時就直接將根節點設為其右子節點
                if(replace==self.root):
                    self.root = self.root.right
                else:
                    #若被刪除的左子樹最小值節點的父節點為葉節點，就代表上面的平衡數值會受到影響，所以必須進行更新
                    if(replace_parent.isLeaf()):
                        self.update_delete_facotr(replace_parent)
                    
                    #若並非為葉子節點，則要進行左轉動作，以保持左子樹最左邊的節點為葉子節點
                    else:
                        self.rotateLeft(replace_parent)
        
        #若要刪除的節點為葉節點
        elif run_node.isLeaf():
            
            #若要刪除的節點為其父節點的左子節點，直接刪除，並因被刪除的是其父節點的左子節點，所以其父節點的平衡點樹應-1
            if(run_node.isLeftChild()):
                run_node.parent.left = None
                run_node.parent.factor-=1
            
            #若要刪除的節點為其父節點的右子節點，直接刪除，並因被刪除的是其父節點的右子節點，所以其父節點的平衡點樹應+1
            else:
                run_node.parent.right = None
                run_node.parent.factor+=1
            
            #若刪除後，其父節點變成葉子節點，則代表上面的平衡數值會受到影響，所以必須進行更新
            if(run_node.parent.isLeaf()):
                self.update_delete_facotr(run_node.parent)
        
        #若要刪除的節點為中介節點
        else:
            #若要刪除的節點數值在根節點的左子樹，則找出左子樹中最小值來替代
            if(self.root.data > data):
                
                #找出左子樹中最小的數值來取代，以符合中序排列
                replace,replace_parent = self.findLeftMin()
                
                #進行取代
                run_node.data = replace.data
                
                #刪除左子樹最小值的節點
                replace_parent.left = None
                
                #因刪除所以要將左子樹最小值節點的父節點之平衡數值-1 (因為刪除的是左子節點)
                replace_parent.factor-=1
                
                #若刪除後，其父節點變成葉子節點，則代表上面的平衡數值會受到影響，所以必須進行更新
                if(replace_parent.isLeaf()):
                    self.update_delete_facotr(replace_parent)
                
                #若其父節點還有右子節點，則必須進行左轉，以確保左子樹最左邊的節點為葉子節點
                else:
                    self.rotateLeft(replace_parent)
            
            #若要刪除的節點數值在根節點的右子樹，則找出右子樹中最大值來替代
            else:
                #找出右子樹中最大的數值來取代，以符合中序排列
                replace,replace_parent = self.findRightMax()
                
                #進行取代
                run_node.data = replace.data
                
                #刪除左子樹最小值的節點
                replace_parent.right = None
                
                #因刪除所以要將右子樹最小值節點的父節點之平衡數值+1 (因為刪除的是右子節點)
                replace_parent.factor+=1
                
                #若刪除後，其父節點變成葉子節點，則代表上面的平衡數值會受到影響，所以必須進行更新
                if(replace_parent.isLeaf()):
                    self.update_delete_facotr(replace_parent)
                
                #若其父節點還有左子節點，則必須進行右轉，以確保右子樹最右邊的節點為葉子節點
                else:
                    self.rotateRight(replace_parent)