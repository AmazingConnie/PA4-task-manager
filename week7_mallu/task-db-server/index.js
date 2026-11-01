// file to run task-db MCP server
// parts of the file were fixed by Claude Code after it found bugs in the original code

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import Database from 'better-sqlite3';
import { z } from 'zod';
import path from 'path';
import { fileURLToPath} from "url";

// Resolve relative to this file (not the cwd), matching where seed.js writes the DB
const here = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.resolve(here, '../task-manager/tasks.db');
const server = new McpServer({
 name: 'task-db-server',
 version: '1.0.0',
});

//  schema for tasks_by_status
const tasks_items = z.object({
    status: z.enum(['open', 'in_progress', 'completed']).describe('Filter tasks by this status value'),
})

//  schema for update_status
const update_items = z.object({
  id: z.number().int().positive().describe('Task ID to update'),
  status: z.enum(['open', 'in_progress', 'completed']).describe('New status value'),
})

// TODO: register tools here

// Filter and return tasks by status
server.tool(
    "tasks_by_status",
    "Return tasks whose status column matches the given value.",
    tasks_items.shape,
    async ({ status }) => {
    // Reject empty input before touching the database
    if (status.trim() === "") {
      throw new Error("status must be a non-empty string");
    }

    const db = new Database(DB_PATH, { readonly: true });
    try {
      // Parameterised query: the ? is filled in safely by the driver
      const rows = db.prepare("SELECT id, title, assigned_to, due_date FROM tasks WHERE status = ? ORDER BY id")
      .all(status);

      // Return false if no tasks are listed for given status
      if (rows.length === 0) {
        return { content: [{ type: "text", text: `No tasks with status: ${status}` }] };
      }

      // else, build table and return it
      const list = rows.map((r) => `${String(r.id).padEnd(3)} | ${r.title.padEnd(25)} | ${(r.assigned_to ?? "").padEnd(11)} | ${r.due_date ?? ""}`);
      const header =  `${"ID".padEnd(3)} | ${"Title".padEnd(25)} | ${"Assigned To".padEnd(11)} | Due Date`;
      const divider = `${"-".repeat(4)}+${"-".repeat(27)}+${"-".repeat(13)}+${"-".repeat(11)}`;
      const table = [header, divider, ...list].join("\n");

      return { content: [{ type: "text", text: table }] };
    } finally {
      db.close();
    }
  }
);

// Find a task by ID and update its status
server.tool("update_task_status",
    "Update status of selected task",
    update_items.shape,
    async ({ id, status }) => {
      const db = new Database(DB_PATH);

      try {
        // Query the table to find the task
        const rows = db.prepare("UPDATE tasks SET status = ? WHERE id = ?").run(status, id);

        // return error statement if task was not found
        if (rows.changes === 0) {
          return { content: [{ type: "text", text: `Task ${id}: not found` }] };
        } 

        // else, return success statement showing the new status of the selected task
        const found = `Task ${id} updated to status: ${status}`;
        return { content: [{ type: "text", text: found }] };

      } finally {
        db.close();
      }
      
    }
  
  
  );

const transport = new StdioServerTransport();
await server.connect(transport);
