# Copilot Instructions for she-calc

## Project Structure
Single-file GUI app in `src/she_calc/__init__.py` for AUTOSAR-SHE MemoryUpdate protocol calculations.

## Critical Patterns

### Component Architecture
```python
class Group(CTkFrame):          # Base titled container
class InputGroup(Group):        # Left panel inputs  
class OutputGroup(Group):       # Right panel results
class App(CTk):                 # Main window orchestrator
```

### Layout System
- `PAD = 10` constant for all spacing
- Two-column grid: inputs left, results right
- Always use `sticky=EW/NSEW/W` for responsive layout
- Access inner content via `Group.frame` property

### Widget Naming Convention
`{type}_{purpose}`: `entry_key`, `combobox_slot`, `textbox_results`, `button_calc`

## Dependencies & Workflow

### Package Management (UV-based)
```bash
uv sync              # Install dependencies
uv run she-calc      # Run via script entry point
uv run python -m she_calc  # Alternative entry point
```

### External Dependencies
- `autosar-she` (git source): Provides `MemorySlot` enum and SHE calculations
- `customtkinter`: Modern GUI components
- Python 3.13+ required

### Development Tools
```bash
uv run mypy src/     # Type checking
uv run pylint src/   # Linting
uv run ruff check    # Fast linting/formatting
```

## Implementation Details

### SHE Integration Pattern
```python
from autosar_she.types import MemorySlot
values=[slot.name for slot in MemorySlot]  # Populate combobox
```

### GUI State Management
- Combobox uses `state="readonly"` for validation
- Results textbox configured as `state="disabled"` after population
- No automatic data binding - manual event handling required

### Adding Button Callbacks
```python
self.button_calc = CTkButton(self, text="Calculate", command=self._on_calculate)
```

### Updating Results Display
```python
self.textbox_results.configure(state="normal")
self.textbox_results.delete("0.0", "end")  
self.textbox_results.insert("0.0", result_text)
self.textbox_results.configure(state="disabled")
```