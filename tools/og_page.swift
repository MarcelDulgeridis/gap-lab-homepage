// Social-Bild je Seite: og_page.swift <ausgabe.png> <kicker> <zeile1> <zeile2> <unterzeile>
import AppKit
let w: CGFloat = 1200, h: CGFloat = 630
let a = CommandLine.arguments
let img = NSImage(size: NSSize(width: w, height: h))
img.lockFocus()
let navy = NSColor(red: 0x10/255, green: 0x1D/255, blue: 0x33/255, alpha: 1)
let navy2 = NSColor(red: 0x1D/255, green: 0x31/255, blue: 0x53/255, alpha: 1)
let gold = NSColor(red: 0xCF/255, green: 0xAD/255, blue: 0x6B/255, alpha: 1)
NSGradient(starting: navy2, ending: navy)!.draw(in: NSRect(x: 0, y: 0, width: w, height: h), angle: -35)
gold.set(); NSRect(x: 0, y: h-10, width: w, height: 10).fill()
func draw(_ s: String, _ size: CGFloat, _ weight: NSFont.Weight, _ color: NSColor, _ x: CGFloat, _ y: CGFloat, kern: CGFloat = 0) {
    let at: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color, .kern: kern]
    NSAttributedString(string: s, attributes: at).draw(at: NSPoint(x: x, y: y))
}
draw("THE GAP LAB", 30, .black, .white, 80, 540, kern: 4)
draw(a[2], 36, .bold, gold, 80, 470, kern: 6)
func fit(_ s: String, _ maxSize: CGFloat, _ maxW: CGFloat) -> CGFloat {
    var size = maxSize
    while size > 40 {
        let at: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: size, weight: .black), .kern: -2]
        if NSAttributedString(string: s, attributes: at).size().width <= maxW { return size }
        size -= 2
    }
    return size
}
let hs = min(fit(a[3], 88, 1040), fit(a[4], 88, 1040))
draw(a[3], hs, .black, .white, 80, 345, kern: -2)
draw(a[4], hs, .black, .white, 80, 250, kern: -2)
gold.set(); NSRect(x: 84, y: 215, width: 120, height: 5).fill()
draw(a[5], 32, .semibold, NSColor(white: 0.9, alpha: 1), 80, 150)
draw("The Gap Lab GmbH · Altdorf bei Nürnberg · gap-lab.de", 26, .regular, gold, 80, 60)
img.unlockFocus()
let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[1]))
