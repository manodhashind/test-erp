// Pure geometry helpers for the hand-rolled dashboard charts (no chart lib in project).

// Smooth cubic-bezier path through a list of [x, y] points.
export function smoothPath(pts) {
	if (pts.length < 2) return ""
	let d = `M${pts[0][0].toFixed(1)},${pts[0][1].toFixed(1)}`
	for (let i = 1; i < pts.length; i++) {
		const cpx = ((pts[i - 1][0] + pts[i][0]) / 2).toFixed(1)
		d += ` C${cpx},${pts[i - 1][1].toFixed(1)} ${cpx},${pts[i][1].toFixed(1)} ${pts[i][0].toFixed(1)},${pts[i][1].toFixed(1)}`
	}
	return d
}
