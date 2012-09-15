import matplotlib.backends.backend_pdf as pdf
import matplotlib.pyplot as plt

pp = pdf.PdfPages("test.pdf")

x=list()
y=list()
for i in range(100):
    x.append(i)
    y.append(i**2)

plt.plot(x,y)
plt.savefig(pp, format='pdf')

plt.figure(2)
plt.clf()
plt.text(0.5,0,"Hello World!")
plt.savefig(pp, format='pdf')


pp.close()