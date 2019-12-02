class AvlNo(object): 
    def __init__(self, pai, k):
        self.valor = k
        self.pai = pai
        self.esquerda = None
        self.direita = None
 
    def _str(self):
        identificador = str(self.valor)
        if self.esquerda is None:
            esquerda_linhas, esquerda_pos, esquerda_largura = [], 0, 0
        else:
            esquerda_linhas, esquerda_pos, esquerda_largura = self.esquerda._str()
        if self.direita is None:
            direita_linhas, direita_pos, direita_largura = [], 0, 0
        else:
            direita_linhas, direita_pos, direita_largura = self.direita._str()
        meio = max(direita_pos + esquerda_largura - esquerda_pos + 1, len(identificador), 2)
        pos = esquerda_pos + meio // 2
        largura = esquerda_pos + meio + direita_largura - direita_pos
        while len(esquerda_linhas) < len(direita_linhas):
            esquerda_linhas.append(' ' * esquerda_largura)
        while len(direita_linhas) < len(esquerda_linhas):
            direita_linhas.append(' ' * direita_largura)
        if (meio - len(identificador)) % 2 == 1 and self.pai is not None and \
           self is self.pai.esquerda and len(identificador) < meio:
            identificador += '.'
        identificador = identificador.center(meio, '.')
        if identificador[0] == '.': identificador = ' ' + identificador[1:]
        if identificador[-1] == '.': identificador = identificador[:-1] + ' '
        linhas = [' ' * esquerda_pos + identificador + ' ' * (direita_largura - direita_pos),
                 ' ' * esquerda_pos + '/' + ' ' * (meio-2) +
                 '\\' + ' ' * (direita_largura - direita_pos)] + \
          [esquerda_linha + ' ' * (largura - esquerda_largura - direita_largura) + direita_linha
           for esquerda_linha, direita_linha in zip(esquerda_linhas, direita_linhas)]
        return linhas, pos, largura
 
    def __str__(self):
        return '\n'.join(self._str()[0])
 
    def busca(self, k):
        if k == self.valor:
            return self
        elif k < self.valor:
            if self.esquerda is None:
                return None
            else:
                return self.esquerda.busca(k)
        else:
            if self.direita is None:  
                return None
            else:
                return self.direita.busca(k)
 
    def buscaMin(self):
        atual = self
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
 
    def proxMaior(self):
        if self.direita is not None:
            return self.direita.buscaMin()
        atual = self
        while atual.pai is not None and atual is atual.pai.direita:
            atual = atual.pai
        return atual.pai
 
    def inserir(self, no):
        if no is None:
            return
        if no.valor < self.valor:
            if self.esquerda is None:
                no.pai = self
                self.esquerda = no
            else:
                self.esquerda.inserir(no)
        else:
            if self.direita is None:
                no.pai = self
                self.direita = no
            else:
                self.direita.inserir(no)
 
    # def delete(self):
    #     if self.esquerda is None or self.direita is None:
    #         if self is self.pai.esquerda:
    #             self.pai.esquerda = self.esquerda or self.direita
    #             if self.pai.esquerda is not None:
    #                 self.pai.esquerda.pai = self.pai
    #         else:
    #             self.pai.direita = self.esquerda or self.direita
    #             if self.pai.direita is not None:
    #                 self.pai.direita.pai = self.pai
    #         return self
    #     else:
    #         s = self.proxMaior()
    #         self.valor, s.valor = s.valor, self.valor
    #         return s.delete()
 
def altura(no):
    if no is None:
        return -1
    else:
        return no.altura
 
def atualizaAltura(no):
    no.altura = max(altura(no.esquerda), altura(no.direita)) + 1

class AVL(object):
    def __init__(self):
        self.raiz = None
 
    def __str__(self):
        if self.raiz is None: return 'Árvore Vazia'
        return str(self.raiz)
 
    def busca(self, k):
        return self.raiz and self.raiz.busca(k)
 
    def buscaMin(self): 
        return self.raiz and self.raiz.buscaMin()
 
    def proxMaior(self, k):
        no = self.busca(k)
        return no and no.proxMaior()   
 
    def rotacaoEsquerda(self, x):
        y = x.direita
        y.pai = x.pai
        if y.pai is None:
            self.raiz = y
        else:
            if y.pai.esquerda is x:
                y.pai.esquerda = y
            elif y.pai.direita is x:
                y.pai.direita = y
        x.direita = y.esquerda
        if x.direita is not None:
            x.direita.pai = x
        y.esquerda = x
        x.pai = y
        atualizaAltura(x)
        atualizaAltura(y)
 
    def rotacaoDireita(self, x):
        y = x.esquerda
        y.pai = x.pai
        if y.pai is None:
            self.raiz = y
        else:
            if y.pai.esquerda is x:
                y.pai.esquerda = y
            elif y.pai.direita is x:
                y.pai.direita = y
        x.esquerda = y.direita
        if x.esquerda is not None:
            x.esquerda.pai = x
        y.direita = x
        x.pai = y
        atualizaAltura(x)
        atualizaAltura(y)
 
    def balanceamento(self, no):
        while no is not None:
            atualizaAltura(no)
            if altura(no.esquerda) >= 2 + altura(no.direita):
                if altura(no.esquerda.esquerda) >= altura(no.esquerda.direita):
                    self.rotacaoDireita(no)
                else:
                    self.rotacaoEsquerda(no.esquerda)
                    self.rotacaoDireita(no)
            elif altura(no.direita) >= 2 + altura(no.esquerda):
                if altura(no.direita.direita) >= altura(no.direita.esquerda):
                    self.rotacaoEsquerda(no)
                else:
                    self.rotacaoDireita(no.direita)
                    self.rotacaoEsquerda(no)
            no = no.pai
 
    def inserir(self, k):
        no = AvlNo(None, k)
        if self.raiz is None:
            self.raiz = no
        else:
            self.raiz.inserir(no)
        self.balanceamento(no)
 
    # def delete(self, k):
    #     no = self.busca(k)
    #     if no is None:
    #         return None
    #     if no is self.raiz:
    #         pseudoraiz = AvlNo(None, 0)
    #         pseudoraiz.esquerda = self.raiz
    #         self.raiz.pai = pseudoraiz
    #         deleted = self.raiz.delete()
    #         self.raiz = pseudoraiz.esquerda
    #         if self.raiz is not None:
    #             self.raiz.pai = None
    #     else:
    #         deleted = no.delete()   
    #     ## no.pai é o antigo pai do no,
    #     ## que provavelmente é o primeiro nó desbalanceado.
    #     self.balanceamento(deleted.pai)
 
def main(args=None):
    import random, sys, time
    if not args:
        args = sys.argv[1:]
    if not args:
        print('Modo de executar o programa: python3 %s [numero de nos aleatorios || nó nó nó nó...]' % \
              sys.argv[0])
        sys.exit()
    elif len(args) == 1:
        itens = (random.randrange(100) for i in range(int(args[0])))
    else:
        itens = [int(i) for i in args]

    inicio = time.time()
    arvore = AVL()
    print(arvore)
    for item in itens:
        arvore.inserir(item)
        print()
        print(arvore)
    fim = time.time()
    decorrido = fim - inicio

    print(decorrido)

if __name__ == '__main__': main()